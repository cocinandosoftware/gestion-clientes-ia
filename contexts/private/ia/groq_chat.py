import json
import re

from django.conf import settings
from groq import Groq
from groq import AuthenticationError, APIConnectionError, RateLimitError

from contexts.private.ia.client_executors import CLIENT_TOOL_EXECUTORS, execute_client_tool
# from contexts.private.ia.prince import PrinceTrace  # Prince desactivado
from contexts.private.ia.tools import CLIENT_SYSTEM_PROMPT, CLIENT_TOOLS
from contexts.private.ia.validation import build_user_messages_text

MAX_TOOL_ROUNDS = 5
KNOWN_CLIENT_TOOLS = set(CLIENT_TOOL_EXECUTORS.keys())
FUNCTION_CALL_IN_CONTENT_RE = re.compile(
    r'<function[=(](\w+)[)>]\s*(\{.*?\})\s*</function>',
    re.DOTALL,
)


class GroqChatError(Exception):
    pass


def _get_groq_client():
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise GroqChatError('La API key de Groq no está configurada.')

    return Groq(api_key=api_key)


def _truncate_detail(value, max_length=140):
    text = str(value)
    if len(text) <= max_length:
        return text
    return f'{text[:max_length]}...'


def _describe_groq_response(assistant_message, tool_calls):
    if tool_calls:
        tool_names = ', '.join(tool_call.function.name for tool_call in tool_calls)
        return f'Groq pidió ejecutar herramientas: {tool_names}'

    content = assistant_message.content or ''
    if '<function' in content:
        return 'Groq devolvió una llamada a función en texto'

    if content:
        return f'Groq devolvió texto: {_truncate_detail(content)}'

    return 'Groq devolvió una respuesta vacía'


def _describe_tool_result(tool_result):
    if tool_result.get('requires_confirmation'):
        return 'Requiere confirmación del usuario'

    if tool_result.get('success'):
        return tool_result.get('message', 'Operación completada')

    return tool_result.get('error', 'La herramienta devolvió un error')


def _create_completion(client, messages, prince, tools=None, tool_choice='auto'):
    try:
        params = {
            'model': settings.GROQ_MODEL,
            'messages': messages,
            'temperature': 0.3,
        }

        if tools is not None:
            params['tools'] = tools
            params['tool_choice'] = tool_choice

        return client.chat.completions.create(**params)
    except AuthenticationError as error:
        raise GroqChatError(
            'La API key de Groq no es válida o ha caducado. '
            'Genera una nueva en console.groq.com y actualiza GROQ_API_KEY en .env.'
        ) from error
    except RateLimitError as error:
        raise GroqChatError(
            'Groq ha rechazado la petición por límite de uso. Inténtalo de nuevo más tarde.'
        ) from error
    except APIConnectionError as error:
        raise GroqChatError(
            'No se pudo conectar con Groq. Comprueba tu conexión a internet.'
        ) from error
    except Exception as error:
        raise GroqChatError('No se pudo obtener respuesta de Groq.') from error


def _serialize_assistant_message(message):
    payload = {
        'role': 'assistant',
        'content': message.content or '',
    }

    if message.tool_calls:
        payload['tool_calls'] = [
            {
                'id': tool_call.id,
                'type': tool_call.type,
                'function': {
                    'name': tool_call.function.name,
                    'arguments': tool_call.function.arguments,
                },
            }
            for tool_call in message.tool_calls
        ]

    return payload


def _parse_function_call_from_content(content):
    if not content:
        return None

    match = FUNCTION_CALL_IN_CONTENT_RE.search(content)
    if not match:
        return None

    tool_name = match.group(1)
    if tool_name not in KNOWN_CLIENT_TOOLS:
        return None

    return tool_name, match.group(2)


def _append_tool_result(messages, tool_call_id, tool_name, arguments, prince, user_messages_text):
    # prince.step(
    #     f'Ejecutando herramienta "{tool_name}"',
    #     _truncate_detail(arguments),
    # )
    tool_result = execute_client_tool(
        tool_name,
        arguments,
        user_messages_text=user_messages_text,
    )
    # prince.step(
    #     f'Resultado de "{tool_name}"',
    #     _describe_tool_result(tool_result),
    # )
    messages.append({
        'role': 'tool',
        'tool_call_id': tool_call_id,
        'content': json.dumps(tool_result, ensure_ascii=False),
    })
    return tool_name


def _execute_parsed_function_call(
    messages,
    tool_name,
    arguments,
    tool_call_id,
    prince,
    user_messages_text,
):
    # prince.step(
    #     f'Función detectada en texto: "{tool_name}"',
    #     'Se convertirá en una llamada a herramienta real',
    # )
    messages.append({
        'role': 'assistant',
        'content': '',
        'tool_calls': [{
            'id': tool_call_id,
            'type': 'function',
            'function': {
                'name': tool_name,
                'arguments': arguments,
            },
        }],
    })
    return _append_tool_result(
        messages,
        tool_call_id,
        tool_name,
        arguments,
        prince,
        user_messages_text,
    )


def _summarize_tool_results(client, messages, intent, prince):
    # prince.step(
    #     'Generando resumen en lenguaje natural',
    #     'Última llamada a Groq sin herramientas',
    # )
    summary_completion = _create_completion(client, messages, prince, tools=None)
    reply = summary_completion.choices[0].message.content
    if not reply:
        raise GroqChatError('Groq devolvió una respuesta vacía tras ejecutar la herramienta.')

    # prince.step(
    #     'Resumen generado por Groq',
    #     _truncate_detail(reply),
    # )

    return {
        'intent': intent,
        'message': reply.strip(),
    }


def process_clients_prompt(user_message, conversation_history=None, prince=None):
    # prince = prince or PrinceTrace()  # Prince desactivado
    client = _get_groq_client()

    messages = [{'role': 'system', 'content': CLIENT_SYSTEM_PROMPT}]

    for entry in conversation_history or []:
        messages.append({
            'role': entry['role'],
            'content': entry['content'],
        })

    messages.append({'role': 'user', 'content': user_message})
    user_messages_text = build_user_messages_text(user_message, conversation_history)

    # prince.step(
    #     'Conversación preparada para Groq',
    #     (
    #         f'{len(conversation_history or [])} mensajes de historial + '
    #         f'mensaje actual ({len(user_message)} caracteres)'
    #     ),
    # )

    intent = 'generic'
    executed_tools = False

    for round_index in range(MAX_TOOL_ROUNDS):
        round_number = round_index + 1
        # prince.step(
        #     f'Enviando petición a Groq (ronda {round_number})',
        #     f'Modelo {settings.GROQ_MODEL} con herramientas activas',
        # )
        completion = _create_completion(client, messages, prince, tools=CLIENT_TOOLS)
        assistant_message = completion.choices[0].message
        tool_calls = assistant_message.tool_calls or []
        # prince.step(
        #     f'Respuesta recibida de Groq (ronda {round_number})',
        #     _describe_groq_response(assistant_message, tool_calls),
        # )

        if not tool_calls:
            parsed_call = _parse_function_call_from_content(assistant_message.content)
            if parsed_call:
                tool_name, arguments = parsed_call
                intent = _execute_parsed_function_call(
                    messages,
                    tool_name,
                    arguments,
                    f'call_parsed_{round_index}',
                    prince,
                    user_messages_text,
                )
                executed_tools = True
                continue

            reply = assistant_message.content
            if not reply:
                if executed_tools:
                    result = _summarize_tool_results(client, messages, intent, prince)
                    # prince.step('Proceso finalizado', f'Intent detectado: {result["intent"]}')
                    return result
                raise GroqChatError('Groq devolvió una respuesta vacía.')

            if '<function' in reply:
                raise GroqChatError(
                    'Groq devolvió una llamada a función sin procesar. Inténtalo de nuevo.'
                )

            # prince.step(
            #     'Respuesta final lista para el usuario',
            #     _truncate_detail(reply),
            # )
            return {
                'intent': intent,
                'message': reply.strip(),
            }

        messages.append(_serialize_assistant_message(assistant_message))
        executed_tools = True

        for tool_call in tool_calls:
            intent = _append_tool_result(
                messages,
                tool_call.id,
                tool_call.function.name,
                tool_call.function.arguments,
                prince,
                user_messages_text,
            )

    if executed_tools:
        result = _summarize_tool_results(client, messages, intent, prince)
        # prince.step('Proceso finalizado', f'Intent detectado: {result["intent"]}')
        return result

    raise GroqChatError('Groq no pudo completar la petición con las herramientas disponibles.')

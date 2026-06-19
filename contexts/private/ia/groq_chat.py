import json

from django.conf import settings
from groq import Groq

from contexts.private.ia.client_executors import execute_client_tool
from contexts.private.ia.tools import CLIENT_SYSTEM_PROMPT, CLIENT_TOOLS


class GroqChatError(Exception):
    pass


def _get_groq_client():
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise GroqChatError('La API key de Groq no está configurada.')

    return Groq(api_key=api_key)


def _create_completion(client, messages, tools=None):
    try:
        params = {
            'model': settings.GROQ_MODEL,
            'messages': messages,
            'temperature': 0.3,
        }

        if tools is not None:
            params['tools'] = tools
            params['tool_choice'] = 'auto'

        return client.chat.completions.create(**params)
    except Exception as error:
        raise GroqChatError('No se pudo obtener respuesta de Groq.') from error


def process_clients_prompt(user_message):
    
    client = _get_groq_client()

    messages = [
        {'role': 'system', 'content': CLIENT_SYSTEM_PROMPT},
        {'role': 'user', 'content': user_message},
    ]

    first_completion = _create_completion(client, messages, tools=CLIENT_TOOLS)
    assistant_message = first_completion.choices[0].message
    tool_calls = assistant_message.tool_calls or []

    if not tool_calls:
        reply = assistant_message.content
        if not reply:
            raise GroqChatError('Groq devolvió una respuesta vacía.')

        return {
            'intent': 'generic',
            'message': reply.strip(),
        }

    messages.append(assistant_message)

    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_result = execute_client_tool(tool_name, tool_call.function.arguments)
        messages.append({
            'role': 'tool',
            'tool_call_id': tool_call.id,
            'content': json.dumps(tool_result, ensure_ascii=False),
        })

    second_completion = _create_completion(client, messages, tools=CLIENT_TOOLS)
    reply = second_completion.choices[0].message.content
    if not reply:
        raise GroqChatError('Groq devolvió una respuesta vacía tras ejecutar la herramienta.')

    return {
        'intent': tool_calls[0].function.name,
        'message': reply.strip(),
    }

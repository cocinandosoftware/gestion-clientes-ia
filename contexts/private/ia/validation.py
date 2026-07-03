import json
import re

AI_PROMPT_MAX_LENGTH = 2000


def validate_ai_prompt(message):
    errors = []

    if not message:
        errors.append('El mensaje no puede estar vacío.')
    elif len(message) > AI_PROMPT_MAX_LENGTH:
        errors.append(f'El mensaje no puede superar los {AI_PROMPT_MAX_LENGTH} caracteres.')

    return errors


def validate_client_id(client_id):
    client_id_text = str(client_id or '').strip()

    if not client_id_text:
        return None, 'Debes indicar el ID del cliente.'

    try:
        parsed_id = int(client_id_text)
    except (TypeError, ValueError):
        return None, 'El ID del cliente no es válido.'

    if parsed_id <= 0:
        return None, 'El ID del cliente no es válido.'

    return parsed_id, None


def build_user_messages_text(user_message, conversation_history=None):
    parts = []

    for entry in conversation_history or []:
        if entry.get('role') == 'user':
            parts.append(str(entry.get('content', '')).strip())

    parts.append(str(user_message or '').strip())
    return '\n'.join(part for part in parts if part)


def user_provided_client_id(user_messages_text, client_id):
    parsed_id, error = validate_client_id(client_id)
    if error:
        return False, error

    pattern = re.compile(rf'(?<!\d){parsed_id}(?!\d)')
    if pattern.search(user_messages_text or ''):
        return True, None

    return False, (
        'Debes indicar el ID del cliente en tu mensaje. '
        'Consúltalo en el listado y escríbelo explícitamente.'
    )


AI_HISTORY_MAX_MESSAGES = 20


def parse_conversation_history(raw_history):
    if not raw_history:
        return []

    try:
        history = json.loads(raw_history)
    except json.JSONDecodeError:
        return []

    if not isinstance(history, list):
        return []

    parsed = []
    for item in history[-AI_HISTORY_MAX_MESSAGES:]:
        if not isinstance(item, dict):
            continue

        role = item.get('role')
        content = str(item.get('content', '')).strip()

        if role in ('user', 'assistant') and content:
            parsed.append({
                'role': role,
                'content': content,
            })

    return parsed

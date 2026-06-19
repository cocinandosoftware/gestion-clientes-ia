import json

AI_PROMPT_MAX_LENGTH = 2000


def validate_ai_prompt(message):
    errors = []

    if not message:
        errors.append('El mensaje no puede estar vacío.')
    elif len(message) > AI_PROMPT_MAX_LENGTH:
        errors.append(f'El mensaje no puede superar los {AI_PROMPT_MAX_LENGTH} caracteres.')

    return errors


def normalize_phone_digits(value):
    return ''.join(character for character in str(value or '') if character.isdigit())


def validate_phone_for_delete(phone):
    phone_text = str(phone or '').strip()

    if not phone_text:
        return None, 'Debes indicar un teléfono válido para eliminar un cliente.'

    digits = normalize_phone_digits(phone_text)

    if len(digits) < 9:
        return None, 'El teléfono indicado no es válido. Debe tener al menos 9 dígitos.'

    if len(digits) > 15:
        return None, 'El teléfono indicado no es válido.'

    return digits, None


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

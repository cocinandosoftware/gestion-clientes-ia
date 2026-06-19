AI_PROMPT_MAX_LENGTH = 2000


def validate_ai_prompt(message):
    errors = []

    if not message:
        errors.append('El mensaje no puede estar vacío.')
    elif len(message) > AI_PROMPT_MAX_LENGTH:
        errors.append(f'El mensaje no puede superar los {AI_PROMPT_MAX_LENGTH} caracteres.')

    return errors

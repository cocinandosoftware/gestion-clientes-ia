from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from contexts.private.ia.groq_chat import GroqChatError, process_clients_prompt
# from contexts.private.ia.prince import PrinceTrace  # Prince desactivado
from contexts.private.ia.validation import parse_conversation_history, validate_ai_prompt


@login_required
@require_POST
def ai_clients_prompt_api_view(request):
    # prince = PrinceTrace.from_settings()  # Prince desactivado
    message = request.POST.get('message', '').strip()
    history = parse_conversation_history(request.POST.get('history', ''))

    # prince.step(
    #     'Mensaje recibido en la API del asistente',
    #     f'"{message[:120]}{"..." if len(message) > 120 else ""}"',
    # )

    errors = validate_ai_prompt(message)
    if errors:
        # prince.step('Validación del mensaje fallida', errors[0])
        return JsonResponse({
            'success': False,
            'errors': errors,
        }, status=400)

    # prince.step('Validación del mensaje completada', 'El mensaje cumple las reglas básicas')
    # prince.step(
    #     'Historial de conversación cargado',
    #     f'{len(history)} mensajes previos en esta sesión',
    # )

    try:
        result = process_clients_prompt(message, history, session=request.session)
    except GroqChatError as error:
        # prince.step('Error en la comunicación con Groq', str(error))
        return JsonResponse({
            'success': False,
            'errors': [str(error)],
        }, status=502)
    except ValueError as error:
        # prince.step('Error al procesar la petición', str(error))
        return JsonResponse({
            'success': False,
            'errors': [str(error)],
        }, status=400)

    return JsonResponse({
        'success': True,
        'intent': result['intent'],
        'message': result['message'],
    })

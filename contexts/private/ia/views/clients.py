from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from contexts.private.ia.validation import validate_ai_prompt


@login_required
@require_POST
def ai_clients_prompt_api_view(request):
    message = request.POST.get('message', '').strip()

    errors = validate_ai_prompt(message)
    if errors:
        return JsonResponse({
            'success': False,
            'errors': errors,
        }, status=400)

    print(f'[IA Clientes] Prompt recibido: {message}')

    return JsonResponse({
        'success': True,
        'message': 'Gracias por tu mensaje.',
    })

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.clients.models import Client


@login_required
@require_POST
def client_delete_view(request, client_id):
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return JsonResponse({
            'success': False,
            'errors': ['El cliente no existe o ya fue eliminado.'],
        }, status=404)

    client_name = client.name
    client.delete()

    return JsonResponse({
        'success': True,
        'message': f'Cliente "{client_name}" eliminado correctamente.',
    })

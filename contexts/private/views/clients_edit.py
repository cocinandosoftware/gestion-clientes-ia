from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.clients.models import Client
from contexts.private.clients.queries import apply_client_payload, serialize_client_form
from contexts.private.clients.validation import REQUIRED_CLIENT_FIELDS, validate_client_payload


@login_required
@require_GET
def client_edit_page_view(request, client_id):
    return render(
        request,
        'private/clients/edit.html',
        {
            'active_menu': 'clients',
            'client_id': client_id,
        },
    )


@login_required
@require_GET
def client_detail_api_view(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    return JsonResponse({
        'success': True,
        'client': serialize_client_form(client),
    })


@login_required
@require_POST
def client_update_api_view(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    data = {
        field: request.POST.get(field, '').strip()
        for field in REQUIRED_CLIENT_FIELDS
    }

    errors = validate_client_payload(data)
    if errors:
        return JsonResponse({
            'success': False,
            'errors': errors,
        }, status=400)

    apply_client_payload(client, data)

    return JsonResponse({
        'success': True,
        'redirect_url': reverse('client_list'),
        'message': 'Cliente actualizado correctamente.',
    })

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.clients.models import Client
from contexts.private.clients.validation import (
    REQUIRED_CLIENT_FIELDS,
    validate_client_payload,
)


@login_required
@require_GET
def client_create_page_view(request):
    return render(
        request,
        'private/clients/create.html',
        {
            'active_menu': 'clients',
        },
    )


@login_required
@require_POST
def client_create_api_view(request):
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

    client_date = datetime.strptime(data['date'], '%Y-%m-%d').date()

    Client.objects.create(
        date=client_date,
        name=data['name'],
        company_name=data['company_name'],
        phone=data['phone'],
        email=data['email'],
        address_line=data['address_line'],
        city=data['city'],
        postal_code=data['postal_code'],
        province=data['province'],
        notes=data['notes'],
    )

    return JsonResponse({
        'success': True,
        'redirect_url': reverse('client_list'),
        'message': 'Cliente creado correctamente.',
    })

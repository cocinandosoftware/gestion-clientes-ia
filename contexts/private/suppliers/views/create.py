from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.suppliers.models import Supplier
from contexts.private.suppliers.queries import parse_client_ids
from contexts.private.suppliers.validation import REQUIRED_SUPPLIER_FIELDS, validate_supplier_payload


@login_required
@require_GET
def supplier_create_page_view(request):
    return render(
        request,
        'private/suppliers/create.html',
        {
            'active_menu': 'suppliers',
        },
    )


@login_required
@require_POST
def supplier_create_api_view(request):
    data = {
        field: request.POST.get(field, '').strip()
        for field in REQUIRED_SUPPLIER_FIELDS
    }
    client_ids = parse_client_ids(request.POST.getlist('clients'))

    errors = validate_supplier_payload(data, client_ids)
    if errors:
        return JsonResponse({
            'success': False,
            'errors': errors,
        }, status=400)

    supplier_date = datetime.strptime(data['date'], '%Y-%m-%d').date()

    supplier = Supplier.objects.create(
        date=supplier_date,
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
    supplier.clients.set(client_ids)

    return JsonResponse({
        'success': True,
        'redirect_url': reverse('supplier_list'),
        'message': 'Proveedor creado correctamente.',
    })

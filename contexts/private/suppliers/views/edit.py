from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.suppliers.models import Supplier
from contexts.private.suppliers.queries import (
    apply_supplier_payload,
    parse_client_ids,
    serialize_supplier_form,
)
from contexts.private.suppliers.validation import REQUIRED_SUPPLIER_FIELDS, validate_supplier_payload


@login_required
@require_GET
def supplier_edit_page_view(request, supplier_id):
    return render(
        request,
        'private/suppliers/edit.html',
        {
            'active_menu': 'suppliers',
            'supplier_id': supplier_id,
        },
    )


@login_required
@require_GET
def supplier_detail_api_view(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)

    return JsonResponse({
        'success': True,
        'supplier': serialize_supplier_form(supplier),
    })


@login_required
@require_POST
def supplier_update_api_view(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)

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

    apply_supplier_payload(supplier, data, client_ids)

    return JsonResponse({
        'success': True,
        'redirect_url': reverse('supplier_list'),
        'message': 'Proveedor actualizado correctamente.',
    })

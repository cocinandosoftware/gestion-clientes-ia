from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from contexts.private.listing import SUPPLIER_SORT_FIELDS, parse_list_request_params
from contexts.private.suppliers.queries import (
    get_client_options,
    get_filtered_suppliers,
    serialize_supplier,
)


@login_required
@require_GET
def supplier_search_view(request):
    list_params = parse_list_request_params(request, SUPPLIER_SORT_FIELDS)

    suppliers, has_filters, pagination = get_filtered_suppliers(
        request.GET.get('q', '').strip(),
        request.GET.get('client_id', '').strip(),
        request.GET.get('date_from', '').strip(),
        request.GET.get('date_until', '').strip(),
        list_params['order_by'],
        list_params['page'],
        list_params['page_size'],
    )

    suppliers_data = [serialize_supplier(supplier) for supplier in suppliers]

    return JsonResponse({
        'success': True,
        'suppliers': suppliers_data,
        'has_filters': has_filters,
        'client_options': get_client_options(),
        'pagination': pagination,
        'sort': {
            'field': list_params['sort_field'],
            'order': list_params['sort_order'],
        },
    })

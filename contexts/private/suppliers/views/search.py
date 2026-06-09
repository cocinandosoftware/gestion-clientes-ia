from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from contexts.private.suppliers.queries import (
    get_client_options,
    get_filtered_suppliers,
    serialize_supplier,
)


@login_required
@require_GET
def supplier_search_view(request):
    search_query = request.GET.get('q', '').strip()
    client_id = request.GET.get('client_id', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_until = request.GET.get('date_until', '').strip()

    suppliers, has_filters = get_filtered_suppliers(
        search_query,
        client_id,
        date_from,
        date_until,
    )

    suppliers_data = [serialize_supplier(supplier) for supplier in suppliers]

    return JsonResponse({
        'success': True,
        'suppliers': suppliers_data,
        'has_filters': has_filters,
        'client_options': get_client_options(),
    })

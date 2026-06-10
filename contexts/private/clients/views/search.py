from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from contexts.private.clients.queries import get_filtered_clients, serialize_client
from contexts.private.listing import CLIENT_SORT_FIELDS, parse_list_request_params


@login_required
@require_GET
def client_search_view(request):
    list_params = parse_list_request_params(request, CLIENT_SORT_FIELDS)

    clients, has_filters, pagination = get_filtered_clients(
        request.GET.get('q', '').strip(),
        request.GET.get('date_from', '').strip(),
        request.GET.get('date_until', '').strip(),
        list_params['order_by'],
        list_params['page'],
        list_params['page_size'],
    )

    clients_data = [serialize_client(client) for client in clients]

    return JsonResponse({
        'success': True,
        'clients': clients_data,
        'has_filters': has_filters,
        'pagination': pagination,
        'sort': {
            'field': list_params['sort_field'],
            'order': list_params['sort_order'],
        },
    })

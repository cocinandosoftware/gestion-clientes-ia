from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from contexts.private.clients.queries import get_filtered_clients, serialize_client


@login_required
@require_GET
def client_search_view(request):
    search_query = request.GET.get('q', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_until = request.GET.get('date_until', '').strip()
    clients, has_filters = get_filtered_clients(search_query, date_from, date_until)

    clients_data = [serialize_client(client) for client in clients]

    return JsonResponse({
        'success': True,
        'clients': clients_data,
        'has_filters': has_filters,
    })

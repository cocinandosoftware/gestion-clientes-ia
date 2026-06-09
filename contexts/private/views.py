from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from core.clients.models import Client


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


@login_required
def welcome_view(request):
    return redirect('client_list')


@login_required
def client_list_view(request):
    
    search_query = request.GET.get('q', '').strip()
    date_from = parse_date(request.GET.get('date_from', '').strip())
    date_until = parse_date(request.GET.get('date_until', '').strip())

    query_filter = Q()

    if search_query:
        query_filter &= (
            Q(name__icontains=search_query)
            | Q(company_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(city__icontains=search_query)
        )

    if date_from:
        query_filter &= Q(date__gte=date_from)

    if date_until:
        query_filter &= Q(date__lte=date_until)

    clients = Client.objects.filter(query_filter)

    return render(
        request,
        'private/clients/list.html',
        {
            'clients': clients,
            'active_menu': 'clients',
            'search_query': search_query,
            'date_from': request.GET.get('date_from', '').strip(),
            'date_until': request.GET.get('date_until', '').strip(),
            'has_filters': search_query or date_from or date_until,
        },
    )

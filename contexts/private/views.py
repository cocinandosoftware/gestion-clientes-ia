from datetime import datetime

from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from config.views import page_not_found
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


def build_list_redirect_params(post_data):
    params = {}
    if post_data.get('q'):
        params['q'] = post_data.get('q')
    if post_data.get('date_from'):
        params['date_from'] = post_data.get('date_from')
    if post_data.get('date_until'):
        params['date_until'] = post_data.get('date_until')
    return params


@login_required
def client_delete_view(request, client_id):
    if request.method != 'POST':
        return redirect('client_list')

    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return page_not_found(request)

    client.delete()

    params = build_list_redirect_params(request.POST)
    if params:
        return redirect(f'{reverse("client_list")}?{urlencode(params)}')
    return redirect('client_list')

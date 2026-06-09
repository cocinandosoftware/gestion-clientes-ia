from datetime import datetime

from django.db.models import Q
from django.urls import reverse

from core.clients.models import Client


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def get_filtered_clients(search_query, date_from_raw, date_until_raw):
    date_from = parse_date(date_from_raw)
    date_until = parse_date(date_until_raw)
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

    has_filters = bool(search_query or date_from or date_until)
    clients = Client.objects.filter(query_filter)

    return clients, has_filters


def serialize_client(client):
    return {
        'id': client.id,
        'name': client.name,
        'company_name': client.company_name,
        'email': client.email,
        'phone': client.phone,
        'city': client.city,
        'date': client.date.strftime('%d/%m/%Y'),
        'delete_url': reverse('client_delete', args=[client.id]),
    }

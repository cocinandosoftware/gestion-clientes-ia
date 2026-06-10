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


def get_filtered_clients(
    search_query,
    date_from_raw,
    date_until_raw,
    order_by,
    page,
    page_size,
):
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
    queryset = Client.objects.filter(query_filter).order_by(order_by)

    from contexts.private.listing import paginate_queryset

    clients, pagination = paginate_queryset(queryset, page, page_size)

    return clients, has_filters, pagination


def serialize_client(client):
    return {
        'id': client.id,
        'name': client.name,
        'company_name': client.company_name,
        'email': client.email,
        'phone': client.phone,
        'city': client.city,
        'date': client.date.strftime('%d/%m/%Y'),
        'edit_url': reverse('client_edit', args=[client.id]),
        'delete_url': reverse('client_delete', args=[client.id]),
    }


def serialize_client_form(client):
    return {
        'id': client.id,
        'date': client.date.strftime('%Y-%m-%d'),
        'name': client.name,
        'company_name': client.company_name,
        'phone': client.phone,
        'email': client.email,
        'address_line': client.address_line,
        'city': client.city,
        'postal_code': client.postal_code,
        'province': client.province,
        'notes': client.notes,
    }


def apply_client_payload(client, data):
    client.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    client.name = data['name']
    client.company_name = data['company_name']
    client.phone = data['phone']
    client.email = data['email']
    client.address_line = data['address_line']
    client.city = data['city']
    client.postal_code = data['postal_code']
    client.province = data['province']
    client.notes = data['notes']
    client.save()

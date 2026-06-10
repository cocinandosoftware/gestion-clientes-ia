from datetime import datetime

from django.db.models import Q
from django.urls import reverse

from core.clients.models import Client
from core.suppliers.models import Supplier


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def parse_client_ids(values):
    client_ids = []

    for value in values:
        try:
            client_ids.append(int(value))
        except ValueError:
            continue

    return client_ids


def get_client_options():
    return [
        {'id': client.id, 'name': client.name}
        for client in Client.objects.order_by('name')
    ]


def get_filtered_suppliers(search_query, client_id_raw, date_from_raw, date_until_raw):
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

    if client_id_raw:
        try:
            client_id = int(client_id_raw)
            query_filter &= Q(clients__id=client_id)
        except ValueError:
            pass

    if date_from:
        query_filter &= Q(date__gte=date_from)

    if date_until:
        query_filter &= Q(date__lte=date_until)

    has_filters = bool(search_query or client_id_raw or date_from or date_until)
    suppliers = Supplier.objects.filter(query_filter).distinct()

    return suppliers, has_filters


CLIENTS_PREVIEW_LIMIT = 2


def format_clients_display(client_names, max_preview=CLIENTS_PREVIEW_LIMIT):
    if not client_names:
        return {
            'clients_label': '',
            'clients_tooltip': '',
            'clients_count': 0,
        }

    full_label = ', '.join(client_names)
    count = len(client_names)

    if count <= max_preview:
        return {
            'clients_label': full_label,
            'clients_tooltip': '',
            'clients_count': count,
        }

    preview = ', '.join(client_names[:max_preview])
    remaining = count - max_preview

    return {
        'clients_label': f'{preview} y {remaining} más',
        'clients_tooltip': full_label,
        'clients_count': count,
    }


def serialize_supplier(supplier):
    client_names = list(supplier.clients.order_by('name').values_list('name', flat=True))
    clients_display = format_clients_display(client_names)

    return {
        'id': supplier.id,
        'name': supplier.name,
        'company_name': supplier.company_name,
        'email': supplier.email,
        'phone': supplier.phone,
        'city': supplier.city,
        'date': supplier.date.strftime('%d/%m/%Y'),
        **clients_display,
        'edit_url': reverse('supplier_edit', args=[supplier.id]),
        'delete_url': reverse('supplier_delete', args=[supplier.id]),
    }


def serialize_supplier_form(supplier):
    return {
        'id': supplier.id,
        'date': supplier.date.strftime('%Y-%m-%d'),
        'name': supplier.name,
        'company_name': supplier.company_name,
        'phone': supplier.phone,
        'email': supplier.email,
        'address_line': supplier.address_line,
        'city': supplier.city,
        'postal_code': supplier.postal_code,
        'province': supplier.province,
        'notes': supplier.notes,
        'client_ids': list(supplier.clients.values_list('id', flat=True)),
    }


def apply_supplier_payload(supplier, data, client_ids):
    supplier.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    supplier.name = data['name']
    supplier.company_name = data['company_name']
    supplier.phone = data['phone']
    supplier.email = data['email']
    supplier.address_line = data['address_line']
    supplier.city = data['city']
    supplier.postal_code = data['postal_code']
    supplier.province = data['province']
    supplier.notes = data['notes']
    supplier.save()
    supplier.clients.set(client_ids)

import json

from core.clients.models import Client

from contexts.private.clients.queries import get_filtered_clients
from contexts.private.ia.validation import normalize_phone_digits, validate_phone_for_delete


def _find_clients_by_phone(phone):
    normalized_phone, phone_error = validate_phone_for_delete(phone)
    if phone_error:
        return None, phone_error

    matches = [
        client
        for client in Client.objects.exclude(phone='')
        if normalize_phone_digits(client.phone) == normalized_phone
    ]

    return matches, None


def _serialize_client_summary(client):
    return {
        'id': client.id,
        'name': client.name,
        'company_name': client.company_name,
        'phone': client.phone,
        'email': client.email,
        'city': client.city,
    }


def execute_search_clients(arguments):
    query = str(arguments.get('query', '')).strip()
    date_from = str(arguments.get('date_from', '')).strip()
    date_until = str(arguments.get('date_until', '')).strip()

    clients, _, pagination = get_filtered_clients(
        query,
        date_from,
        date_until,
        'name',
        1,
        10,
    )

    return {
        'success': True,
        'total_count': pagination['total_count'],
        'shown_count': len(clients),
        'clients': [
            {
                'name': client.name,
                'company_name': client.company_name,
                'email': client.email,
                'phone': client.phone,
                'city': client.city,
                'date': client.date.strftime('%d/%m/%Y'),
            }
            for client in clients
        ],
    }


def execute_delete_client(arguments):
    phone = str(arguments.get('phone', '')).strip()
    confirmed = bool(arguments.get('confirmed', False))

    matches, lookup_error = _find_clients_by_phone(phone)
    if lookup_error:
        return {
            'success': False,
            'error': lookup_error,
        }

    if not matches:
        return {
            'success': False,
            'error': 'No se encontró ningún cliente con ese teléfono.',
        }

    if len(matches) > 1:
        return {
            'success': False,
            'error': (
                'Hay varios clientes con ese teléfono. '
                'No se puede eliminar automáticamente.'
            ),
        }

    client = matches[0]

    if not confirmed:
        return {
            'success': False,
            'requires_confirmation': True,
            'client': _serialize_client_summary(client),
            'message': (
                f'Se ha localizado al cliente "{client.name}" con teléfono {client.phone}. '
                'Pide confirmación explícita antes de eliminar.'
            ),
        }

    deleted_client = _serialize_client_summary(client)
    client.delete()

    return {
        'success': True,
        'deleted_client': deleted_client,
        'message': (
            f'Cliente "{deleted_client["name"]}" eliminado correctamente '
            f'con teléfono {deleted_client["phone"]}.'
        ),
    }


CLIENT_TOOL_EXECUTORS = {
    'search_clients': execute_search_clients,
    'delete_client': execute_delete_client,
}


def execute_client_tool(tool_name, arguments):
    executor = CLIENT_TOOL_EXECUTORS.get(tool_name)
    if not executor:
        raise ValueError(f'Herramienta no soportada: {tool_name}')

    if isinstance(arguments, str):
        arguments = json.loads(arguments or '{}')

    return executor(arguments or {})

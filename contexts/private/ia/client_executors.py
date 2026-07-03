import json

from core.clients.models import Client

from contexts.private.clients.queries import (
    apply_client_payload,
    create_client_from_payload,
    get_filtered_clients,
    serialize_client_form,
)
from contexts.private.clients.validation import (
    CLIENT_FIELD_LABELS,
    REQUIRED_CLIENT_FIELDS,
    validate_client_payload,
    validate_client_unique_contact,
)
from contexts.private.ia.validation import user_provided_client_id, validate_client_id


def _require_user_provided_client_id(client_id, user_messages_text):
    is_provided, error = user_provided_client_id(user_messages_text, client_id)
    if not is_provided:
        return error
    return None


def _find_client_by_id(client_id):
    parsed_id, lookup_error = validate_client_id(client_id)
    if lookup_error:
        return None, lookup_error

    client = Client.objects.filter(pk=parsed_id).first()
    if not client:
        return None, f'No se encontró ningún cliente con ID {parsed_id}.'

    return client, None


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
                'id': client.id,
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


def _extract_client_payload(arguments):
    payload = {}

    for field in REQUIRED_CLIENT_FIELDS:
        if field in arguments and arguments[field] is not None:
            payload[field] = str(arguments[field]).strip()
        else:
            payload[field] = ''

    return payload


def _extract_client_updates(arguments):
    updates = {}

    for field in REQUIRED_CLIENT_FIELDS:
        if field in arguments and arguments[field] is not None:
            value = str(arguments[field]).strip()
            if value:
                updates[field] = value

    return updates


def _build_client_changes(current_data, merged_data):
    changes = {}

    for field in REQUIRED_CLIENT_FIELDS:
        old_value = current_data.get(field, '')
        new_value = merged_data.get(field, '')
        if old_value != new_value:
            changes[field] = {
                'label': CLIENT_FIELD_LABELS[field],
                'from': old_value,
                'to': new_value,
            }

    return changes


def execute_update_client(arguments, user_messages_text=''):
    client_id = arguments.get('client_id')
    confirmed = bool(arguments.get('confirmed', False))
    updates = _extract_client_updates(arguments)

    id_error = _require_user_provided_client_id(client_id, user_messages_text)
    if id_error:
        return {
            'success': False,
            'error': id_error,
        }

    if not updates:
        return {
            'success': False,
            'error': 'Debes indicar al menos un campo para actualizar.',
        }

    client, lookup_error = _find_client_by_id(client_id)
    if lookup_error:
        return {
            'success': False,
            'error': lookup_error,
        }

    current_data = serialize_client_form(client)
    merged_data = {field: current_data[field] for field in REQUIRED_CLIENT_FIELDS}
    merged_data.update(updates)

    errors = validate_client_payload(merged_data)
    if errors:
        return {
            'success': False,
            'error': errors[0],
        }

    unique_errors = validate_client_unique_contact(
        merged_data,
        exclude_client_id=client.id,
    )
    if unique_errors:
        return {
            'success': False,
            'error': unique_errors[0],
        }

    changes = _build_client_changes(current_data, merged_data)
    if not changes:
        return {
            'success': False,
            'error': 'Los valores indicados ya coinciden con la ficha del cliente.',
        }

    if not confirmed:
        return {
            'success': False,
            'requires_confirmation': True,
            'client': _serialize_client_summary(client),
            'changes': changes,
            'message': (
                f'Se ha localizado al cliente "{client.name}" con ID {client.id}. '
                'Resume los cambios y pide confirmación explícita antes de actualizar.'
            ),
        }

    apply_client_payload(client, merged_data)
    updated_client = serialize_client_form(client)

    return {
        'success': True,
        'updated_client': updated_client,
        'changes': changes,
        'message': (
            f'Cliente "{updated_client["name"]}" (ID {updated_client["id"]}) '
            'actualizado correctamente.'
        ),
    }


def execute_delete_client(arguments, user_messages_text=''):
    client_id = arguments.get('client_id')
    confirmed = bool(arguments.get('confirmed', False))

    id_error = _require_user_provided_client_id(client_id, user_messages_text)
    if id_error:
        return {
            'success': False,
            'error': id_error,
        }

    client, lookup_error = _find_client_by_id(client_id)
    if lookup_error:
        return {
            'success': False,
            'error': lookup_error,
        }

    if not confirmed:
        return {
            'success': False,
            'requires_confirmation': True,
            'client': _serialize_client_summary(client),
            'message': (
                f'Se ha localizado al cliente "{client.name}" con ID {client.id}. '
                'Pide confirmación explícita antes de eliminar.'
            ),
        }

    deleted_client = _serialize_client_summary(client)
    client.delete()

    return {
        'success': True,
        'deleted_client': deleted_client,
        'message': (
            f'Cliente "{deleted_client["name"]}" (ID {deleted_client["id"]}) '
            'eliminado correctamente.'
        ),
    }


def execute_create_client(arguments):
    confirmed = bool(arguments.get('confirmed', False))
    payload = _extract_client_payload(arguments)

    errors = validate_client_payload(payload)
    if errors:
        return {
            'success': False,
            'error': errors[0],
        }

    unique_errors = validate_client_unique_contact(payload)
    if unique_errors:
        return {
            'success': False,
            'error': unique_errors[0],
        }

    preview = {
        field: payload[field]
        for field in REQUIRED_CLIENT_FIELDS
    }

    if not confirmed:
        return {
            'success': False,
            'requires_confirmation': True,
            'client_preview': preview,
            'message': (
                'Resume los datos del nuevo cliente y pide confirmación explícita '
                'antes de crearlo.'
            ),
        }

    client = create_client_from_payload(payload)
    created_client = serialize_client_form(client)

    return {
        'success': True,
        'created_client': created_client,
        'message': (
            f'Cliente "{created_client["name"]}" (ID {created_client["id"]}) '
            'creado correctamente.'
        ),
    }


CLIENT_TOOL_EXECUTORS = {
    'search_clients': execute_search_clients,
    'create_client': execute_create_client,
    'update_client': execute_update_client,
    'delete_client': execute_delete_client,
}


def execute_client_tool(tool_name, arguments, user_messages_text=''):
    executor = CLIENT_TOOL_EXECUTORS.get(tool_name)
    if not executor:
        raise ValueError(f'Herramienta no soportada: {tool_name}')

    if isinstance(arguments, str):
        arguments = json.loads(arguments or '{}')

    arguments = arguments or {}

    if tool_name in ('update_client', 'delete_client'):
        return executor(arguments, user_messages_text=user_messages_text)

    return executor(arguments)

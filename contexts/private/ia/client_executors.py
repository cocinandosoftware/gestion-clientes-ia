import json

from contexts.private.clients.queries import get_filtered_clients


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


CLIENT_TOOL_EXECUTORS = {
    'search_clients': execute_search_clients,
}


def execute_client_tool(tool_name, arguments):
    executor = CLIENT_TOOL_EXECUTORS.get(tool_name)
    if not executor:
        raise ValueError(f'Herramienta no soportada: {tool_name}')

    if isinstance(arguments, str):
        arguments = json.loads(arguments or '{}')

    return executor(arguments or {})

CLIENT_TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'search_clients',
            'description': (
                'Busca clientes en la base de datos del sistema. '
                'Úsala cuando el usuario quiera encontrar, listar o consultar clientes '
                'por nombre, email, teléfono, empresa, ciudad o rango de fechas.'
            ),
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': (
                            'Texto libre para buscar en nombre, email, teléfono, '
                            'razón social o ciudad.'
                        ),
                    },
                    'date_from': {
                        'type': 'string',
                        'description': 'Fecha mínima de alta del cliente (YYYY-MM-DD).',
                    },
                    'date_until': {
                        'type': 'string',
                        'description': 'Fecha máxima de alta del cliente (YYYY-MM-DD).',
                    },
                },
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'delete_client',
            'description': (
                'Elimina un cliente identificado de forma única por su teléfono. '
                'Úsala solo cuando el usuario pida eliminar un cliente y haya '
                'indicado un número de teléfono válido.'
            ),
            'parameters': {
                'type': 'object',
                'properties': {
                    'phone': {
                        'type': 'string',
                        'description': (
                            'Teléfono del cliente a eliminar. Debe ser un número válido '
                            'con al menos 9 dígitos.'
                        ),
                    },
                    'confirmed': {
                        'type': 'boolean',
                        'description': (
                            'Debe ser true solo si el usuario ha confirmado explícitamente '
                            'la eliminación tras ver qué cliente se va a borrar.'
                        ),
                    },
                },
                'required': ['phone'],
            },
        },
    },
]

CLIENT_SYSTEM_PROMPT = """Eres un asistente del sistema de gestión de clientes.

Tienes acceso a herramientas para consultar y eliminar clientes registrados.

Reglas:
- Si el usuario pregunta sobre clientes (buscar, listar, consultar quién hay, filtrar por ciudad, etc.), usa search_clients.
- Si el usuario pide eliminar un cliente, usa delete_client solo si ha indicado un teléfono válido en su mensaje.
- Nunca llames a delete_client sin el parámetro phone con un teléfono real extraído del mensaje del usuario.
- Para eliminar: primero localiza al cliente con phone y confirmed=false. Pide confirmación explícita al usuario.
- Solo vuelve a llamar a delete_client con confirmed=true si el usuario responde claramente que sí, confirmo o similar.
- Si la herramienta devuelve error o requires_confirmation, explica el resultado al usuario sin inventar datos.
- Si la pregunta es genérica (saludos, definiciones, temas ajenos a clientes), responde sin usar herramientas.
- Resume los resultados en español de forma clara y breve.

Responde siempre en español."""

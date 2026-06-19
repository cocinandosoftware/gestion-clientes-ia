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
]

CLIENT_SYSTEM_PROMPT = """Eres un asistente del sistema de gestión de clientes.

Tienes acceso a herramientas para consultar datos reales de clientes registrados.

Reglas:
- Si el usuario pregunta sobre clientes (buscar, listar, consultar quién hay, filtrar por ciudad, etc.), usa la herramienta search_clients.
- Si la pregunta es genérica (saludos, definiciones, temas ajenos a clientes del sistema), responde directamente sin usar herramientas.
- Cuando uses una herramienta, resume los resultados en español de forma clara y breve.
- Si no hay resultados, dilo explícitamente.

Responde siempre en español."""

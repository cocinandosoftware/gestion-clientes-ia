CLIENT_TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'search_clients',
            'description': (
                'Busca clientes en la base de datos del sistema. '
                'Úsala solo para consultar o listar clientes. '
                'Acepta texto libre o un ID numérico para localizar un cliente concreto. '
                'No uses sus resultados para ejecutar actualizaciones ni eliminaciones.'
            ),
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': (
                            'Texto libre para buscar en nombre, email, teléfono, '
                            'razón social o ciudad. Si es un número, también busca por ID.'
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
            'name': 'update_client',
            'description': (
                'Actualiza uno o varios campos de la ficha de un cliente. '
                'Solo si el usuario ha escrito explícitamente el ID del cliente en su mensaje.'
            ),
            'parameters': {
                'type': 'object',
                'properties': {
                    'client_id': {
                        'type': 'integer',
                        'description': (
                            'ID numérico del cliente a actualizar. '
                            'Debe haber sido escrito por el usuario en su mensaje.'
                        ),
                    },
                    'confirmed': {
                        'type': 'boolean',
                        'description': (
                            'Debe ser true solo si el usuario ha confirmado explícitamente '
                            'los cambios tras ver qué campos se van a modificar.'
                        ),
                    },
                    'date': {
                        'type': 'string',
                        'description': 'Nueva fecha de alta del cliente (YYYY-MM-DD).',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'Nuevo nombre del cliente.',
                    },
                    'company_name': {
                        'type': 'string',
                        'description': 'Nueva razón social del cliente.',
                    },
                    'phone': {
                        'type': 'string',
                        'description': 'Nuevo teléfono del cliente.',
                    },
                    'email': {
                        'type': 'string',
                        'description': 'Nuevo email del cliente.',
                    },
                    'address_line': {
                        'type': 'string',
                        'description': 'Nueva dirección del cliente.',
                    },
                    'city': {
                        'type': 'string',
                        'description': 'Nueva ciudad del cliente.',
                    },
                    'postal_code': {
                        'type': 'string',
                        'description': 'Nuevo código postal del cliente.',
                    },
                    'province': {
                        'type': 'string',
                        'description': 'Nueva provincia del cliente.',
                    },
                    'notes': {
                        'type': 'string',
                        'description': 'Nuevas notas del cliente.',
                    },
                },
                'required': ['client_id'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'delete_client',
            'description': (
                'Elimina un cliente por su ID. '
                'Solo si el usuario ha escrito explícitamente el ID del cliente en su mensaje.'
            ),
            'parameters': {
                'type': 'object',
                'properties': {
                    'client_id': {
                        'type': 'integer',
                        'description': (
                            'ID numérico del cliente a eliminar. '
                            'Debe haber sido escrito por el usuario en su mensaje.'
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
                'required': ['client_id'],
            },
        },
    },
]

CLIENT_SYSTEM_PROMPT = """Eres un asistente del sistema de gestión de clientes.

Tienes acceso a herramientas para consultar, actualizar y eliminar clientes registrados.

Reglas:
- Si el usuario pregunta sobre clientes (buscar, listar, consultar quién hay, filtrar por ciudad, etc.), usa search_clients.
- search_clients es solo para consulta. Muestra el ID de cada cliente para que el usuario lo vea en el listado, pero no lo uses tú para actualizar ni eliminar.
- Para actualizar o eliminar, el usuario DEBE escribir el ID en su mensaje. El ID lo proporciona el usuario, no el asistente.
- Nunca deduzcas, busques ni infieras el ID a partir del teléfono, nombre, email u otros datos.
- Nunca encadenes search_clients con update_client ni delete_client en la misma petición.
- Si el usuario pide actualizar o eliminar sin indicar un ID numérico en su mensaje, responde sin herramientas pidiéndole que consulte el listado y escriba el ID explícitamente.
- Si el usuario pide modificar datos de un cliente, usa update_client solo cuando su mensaje (o un mensaje previo suyo en la conversación) contenga el ID numérico.
- Nunca llames a update_client con un client_id que el usuario no haya escrito explícitamente.
- En update_client solo envía los campos que el usuario quiere cambiar. No rellenes campos que no haya pedido modificar.
- Para actualizar: primero localiza al cliente con client_id, los cambios solicitados y confirmed=false. Resume los cambios y pide confirmación explícita.
- Solo vuelve a llamar a update_client con confirmed=true si el usuario responde claramente que sí, confirmo o similar.
- Si el usuario pide eliminar un cliente, usa delete_client solo cuando su mensaje (o un mensaje previo suyo en la conversación) contenga el ID numérico.
- Nunca llames a delete_client con un client_id que el usuario no haya escrito explícitamente.
- Para eliminar: primero localiza al cliente con client_id y confirmed=false. Pide confirmación explícita al usuario.
- Solo vuelve a llamar a delete_client con confirmed=true si el usuario responde claramente que sí, confirmo o similar.
- Si la herramienta devuelve error o requires_confirmation, explica el resultado al usuario sin inventar datos.
- Nunca escribas llamadas a funciones en texto (por ejemplo <function=...>). Usa siempre las herramientas del sistema.
- Si la pregunta es genérica (saludos, definiciones, temas ajenos a clientes), responde sin usar herramientas.
- Resume los resultados en español de forma clara y breve.

Responde siempre en español."""

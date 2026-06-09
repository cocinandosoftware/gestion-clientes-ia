from datetime import datetime

from core.clients.models import Client

SUPPLIER_FIELD_LABELS = {
    'date': 'fecha',
    'name': 'nombre',
    'company_name': 'razón social',
    'phone': 'teléfono',
    'email': 'email',
    'address_line': 'dirección',
    'city': 'ciudad',
    'postal_code': 'código postal',
    'province': 'provincia',
    'notes': 'notas',
}

REQUIRED_SUPPLIER_FIELDS = tuple(SUPPLIER_FIELD_LABELS.keys())


def validate_supplier_payload(data, client_ids):
    errors = []

    for field in REQUIRED_SUPPLIER_FIELDS:
        if not str(data.get(field, '')).strip():
            errors.append(f'El campo {SUPPLIER_FIELD_LABELS[field]} es obligatorio.')

    if not client_ids:
        errors.append('Debes seleccionar al menos un cliente asociado.')

    if errors:
        return errors

    email = data.get('email', '').strip()
    if '@' not in email or '.' not in email.split('@')[-1]:
        errors.append('El email no es válido.')

    try:
        datetime.strptime(data.get('date', '').strip(), '%Y-%m-%d')
    except ValueError:
        errors.append('La fecha no es válida.')

    valid_client_ids = set(
        Client.objects.filter(pk__in=client_ids).values_list('pk', flat=True)
    )
    invalid_ids = [client_id for client_id in client_ids if client_id not in valid_client_ids]

    if invalid_ids:
        errors.append('Uno o más clientes seleccionados no son válidos.')

    return errors

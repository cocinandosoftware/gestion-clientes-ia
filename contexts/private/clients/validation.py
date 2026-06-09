from datetime import datetime

CLIENT_FIELD_LABELS = {
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

REQUIRED_CLIENT_FIELDS = tuple(CLIENT_FIELD_LABELS.keys())


def validate_client_payload(data):
    errors = []

    for field in REQUIRED_CLIENT_FIELDS:
        if not str(data.get(field, '')).strip():
            errors.append(f'El campo {CLIENT_FIELD_LABELS[field]} es obligatorio.')

    if errors:
        return errors

    email = data.get('email', '').strip()
    if '@' not in email or '.' not in email.split('@')[-1]:
        errors.append('El email no es válido.')

    try:
        datetime.strptime(data.get('date', '').strip(), '%Y-%m-%d')
    except ValueError:
        errors.append('La fecha no es válida.')

    return errors

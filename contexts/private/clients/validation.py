from datetime import datetime

from core.clients.models import Client

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


def get_missing_client_fields(data):
    return [
        field
        for field in REQUIRED_CLIENT_FIELDS
        if not str(data.get(field, '')).strip()
    ]


def get_collected_client_fields(data):
    return {
        field: str(data.get(field, '')).strip()
        for field in REQUIRED_CLIENT_FIELDS
        if str(data.get(field, '')).strip()
    }


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


def validate_client_unique_contact(data, exclude_client_id=None):
    errors = []
    phone = str(data.get('phone', '')).strip()
    email = str(data.get('email', '')).strip()

    if phone:
        phone_queryset = Client.objects.filter(phone=phone)
        if exclude_client_id:
            phone_queryset = phone_queryset.exclude(pk=exclude_client_id)
        if phone_queryset.exists():
            errors.append('Ya existe un cliente con ese teléfono.')

    if email:
        email_queryset = Client.objects.filter(email__iexact=email)
        if exclude_client_id:
            email_queryset = email_queryset.exclude(pk=exclude_client_id)
        if email_queryset.exists():
            errors.append('Ya existe un cliente con ese email.')

    return errors

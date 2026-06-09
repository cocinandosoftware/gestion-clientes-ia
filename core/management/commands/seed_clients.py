import json
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand

from core.clients.models import Client

DEFAULT_JSON = (
    Path(__file__).resolve().parent.parent.parent
    / 'clients'
    / 'data'
    / 'clients_seed.json'
)

TEXT_FIELDS = (
    'name',
    'company_name',
    'phone',
    'email',
    'address_line',
    'city',
    'postal_code',
    'province',
    'notes',
)

DATE_FIELDS = ('date',)


class Command(BaseCommand):
    help = 'Carga clientes de ejemplo desde un archivo JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=str(DEFAULT_JSON),
            help='Ruta al archivo JSON de clientes',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los clientes antes de cargar',
        )

    def handle(self, *args, **options):
        json_path = Path(options['file'])

        if not json_path.exists():
            self.stderr.write(self.style.ERROR(f'Archivo no encontrado: {json_path}'))
            return

        with json_path.open(encoding='utf-8') as file:
            clients_data = json.load(file)

        if options['clear']:
            deleted, _ = Client.objects.all().delete()
            self.stdout.write(f'Eliminados {deleted} clientes existentes.')

        created_count = 0

        for item in clients_data:
            client_fields = {field: item.get(field, '') for field in TEXT_FIELDS}

            for field in DATE_FIELDS:
                date_value = item.get(field)
                if not date_value:
                    self.stderr.write(
                        self.style.WARNING(
                            f'Cliente "{item.get("name", "sin nombre")}" sin fecha. Omitido.'
                        )
                    )
                    break
                client_fields[field] = datetime.strptime(date_value, '%Y-%m-%d').date()
            else:
                Client.objects.create(**client_fields)
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Carga completada: {created_count} clientes creados.')
        )

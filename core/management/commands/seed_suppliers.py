import json
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand

from core.clients.models import Client
from core.suppliers.models import Supplier

DEFAULT_JSON = (
    Path(__file__).resolve().parent.parent.parent
    / 'suppliers'
    / 'data'
    / 'suppliers_seed.json'
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
    help = 'Carga proveedores de ejemplo desde un archivo JSON organizado por cliente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=str(DEFAULT_JSON),
            help='Ruta al archivo JSON de proveedores',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los proveedores antes de cargar',
        )

    def handle(self, *args, **options):
        json_path = Path(options['file'])

        if not json_path.exists():
            self.stderr.write(self.style.ERROR(f'Archivo no encontrado: {json_path}'))
            return

        with json_path.open(encoding='utf-8') as file:
            suppliers_data = json.load(file)

        if options['clear']:
            deleted, _ = Supplier.objects.all().delete()
            self.stdout.write(f'Eliminados {deleted} proveedores existentes.')

        created_count = 0
        linked_count = 0

        for group in suppliers_data:
            client_email = group.get('client_email', '').strip()
            client = Client.objects.filter(email=client_email).first()

            if not client:
                self.stderr.write(
                    self.style.WARNING(
                        f'Cliente con email "{client_email}" no encontrado. Grupo omitido.'
                    )
                )
                continue

            for item in group.get('suppliers', []):
                supplier_fields = {field: item.get(field, '') for field in TEXT_FIELDS}

                for field in DATE_FIELDS:
                    date_value = item.get(field)
                    if not date_value:
                        self.stderr.write(
                            self.style.WARNING(
                                f'Proveedor "{item.get("name", "sin nombre")}" sin fecha. Omitido.'
                            )
                        )
                        break
                    supplier_fields[field] = datetime.strptime(date_value, '%Y-%m-%d').date()
                else:
                    supplier_email = supplier_fields.get('email', '').strip()
                    supplier = None

                    if supplier_email:
                        supplier = Supplier.objects.filter(email=supplier_email).first()

                    if supplier:
                        for field, value in supplier_fields.items():
                            setattr(supplier, field, value)
                        supplier.save()
                    else:
                        supplier = Supplier.objects.create(**supplier_fields)
                        created_count += 1

                    supplier.clients.add(client)
                    linked_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Carga completada: {created_count} proveedores nuevos, '
                f'{linked_count} vínculos con clientes.'
            )
        )

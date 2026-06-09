from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.clients import admin as clients_admin  # noqa: F401
        from core.users import admin as users_admin  # noqa: F401

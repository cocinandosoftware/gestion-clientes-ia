from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Modelo de usuario del sistema."""

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

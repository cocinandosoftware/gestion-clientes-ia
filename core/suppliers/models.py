from django.db import models
from django.utils import timezone

from core.clients.models import Client


class Supplier(models.Model):

    date = models.DateField('fecha', default=timezone.now)
    name = models.CharField('nombre', max_length=200)
    company_name = models.CharField('razón social', max_length=200, blank=True)
    phone = models.CharField('teléfono', max_length=30, blank=True)
    email = models.EmailField('email', blank=True)
    address_line = models.CharField('dirección', max_length=255, blank=True)
    city = models.CharField('ciudad', max_length=100, blank=True)
    postal_code = models.CharField('código postal', max_length=10, blank=True)
    province = models.CharField('provincia', max_length=100, blank=True)
    notes = models.TextField('notas', blank=True)
    clients = models.ManyToManyField(
        Client,
        related_name='suppliers',
        verbose_name='clientes',
    )
    created_at = models.DateTimeField('creado', auto_now_add=True)
    updated_at = models.DateTimeField('actualizado', auto_now=True)

    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

from django.urls import include, path

from .welcome import welcome_view

urlpatterns = [
    path('', welcome_view, name='private_welcome'),
    path('ia/', include('contexts.private.ia.urls')),
    path('clientes/', include('contexts.private.clients.urls')),
    path('proveedores/', include('contexts.private.suppliers.urls')),
]

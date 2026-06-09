from django.urls import path

from . import views

urlpatterns = [
    path('private/', views.welcome_view, name='private_welcome'),
    path('private/clientes/', views.client_list_view, name='client_list'),
]

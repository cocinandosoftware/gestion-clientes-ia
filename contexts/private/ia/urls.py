from django.urls import path

from .views.clients import ai_clients_prompt_api_view

urlpatterns = [
    path('clientes/enviar/', ai_clients_prompt_api_view, name='ai_clients_prompt'),
]

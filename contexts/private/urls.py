from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_view, name='private_welcome'),
    path('clientes/', views.client_list_view, name='client_list'),
    path('clientes/buscar/', views.client_search_view, name='client_search'),
    path('clientes/<int:client_id>/eliminar/', views.client_delete_view, name='client_delete'),
]

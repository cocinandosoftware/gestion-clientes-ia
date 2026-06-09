from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_view, name='private_welcome'),
    path('clientes/', views.client_list_view, name='client_list'),
    path('clientes/nuevo/', views.client_create_page_view, name='client_create'),
    path('clientes/crear/', views.client_create_api_view, name='client_create_api'),
    path('clientes/buscar/', views.client_search_view, name='client_search'),
    path('clientes/<int:client_id>/eliminar/', views.client_delete_view, name='client_delete'),
]

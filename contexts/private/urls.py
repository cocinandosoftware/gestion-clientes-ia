from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_view, name='private_welcome'),
    path('clientes/', views.client_list_view, name='client_list'),
]

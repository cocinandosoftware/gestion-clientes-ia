from django.urls import path

from . import views

urlpatterns = [
    path('private/', views.welcome_view, name='private_welcome'),
]

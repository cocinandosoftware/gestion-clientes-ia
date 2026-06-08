from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/validate/', views.login_validate_view, name='login_validate'),
    path('logout/', views.logout_view, name='logout'),
]

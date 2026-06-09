from django.urls import path

from .views.create import client_create_api_view, client_create_page_view
from .views.delete import client_delete_view
from .views.edit import (
    client_detail_api_view,
    client_edit_page_view,
    client_update_api_view,
)
from .views.list import client_list_view
from .views.search import client_search_view

urlpatterns = [
    path('', client_list_view, name='client_list'),
    path('nuevo/', client_create_page_view, name='client_create'),
    path('crear/', client_create_api_view, name='client_create_api'),
    path('buscar/', client_search_view, name='client_search'),
    path('<int:client_id>/editar/', client_edit_page_view, name='client_edit'),
    path('<int:client_id>/detalle/', client_detail_api_view, name='client_detail'),
    path('<int:client_id>/actualizar/', client_update_api_view, name='client_update'),
    path('<int:client_id>/eliminar/', client_delete_view, name='client_delete'),
]

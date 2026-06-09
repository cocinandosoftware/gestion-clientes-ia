from django.urls import path

from .views.create import supplier_create_api_view, supplier_create_page_view
from .views.delete import supplier_delete_view
from .views.edit import (
    supplier_detail_api_view,
    supplier_edit_page_view,
    supplier_update_api_view,
)
from .views.list import supplier_list_view
from .views.search import supplier_search_view

urlpatterns = [
    path('', supplier_list_view, name='supplier_list'),
    path('nuevo/', supplier_create_page_view, name='supplier_create'),
    path('crear/', supplier_create_api_view, name='supplier_create_api'),
    path('buscar/', supplier_search_view, name='supplier_search'),
    path('<int:supplier_id>/editar/', supplier_edit_page_view, name='supplier_edit'),
    path('<int:supplier_id>/detalle/', supplier_detail_api_view, name='supplier_detail'),
    path('<int:supplier_id>/actualizar/', supplier_update_api_view, name='supplier_update'),
    path('<int:supplier_id>/eliminar/', supplier_delete_view, name='supplier_delete'),
]

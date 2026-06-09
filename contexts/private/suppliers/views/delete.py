from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.suppliers.models import Supplier


@login_required
@require_POST
def supplier_delete_view(request, supplier_id):
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
    except Supplier.DoesNotExist:
        return JsonResponse({
            'success': False,
            'errors': ['El proveedor no existe o ya fue eliminado.'],
        }, status=404)

    supplier_name = supplier.name
    supplier.delete()

    return JsonResponse({
        'success': True,
        'message': f'Proveedor "{supplier_name}" eliminado correctamente.',
    })

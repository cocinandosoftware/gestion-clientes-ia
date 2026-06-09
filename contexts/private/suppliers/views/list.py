from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def supplier_list_view(request):
    return render(
        request,
        'private/suppliers/list.html',
        {
            'active_menu': 'suppliers',
        },
    )

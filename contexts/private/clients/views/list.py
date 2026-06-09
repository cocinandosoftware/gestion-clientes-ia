from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def client_list_view(request):
    return render(
        request,
        'private/clients/list.html',
        {
            'active_menu': 'clients',
        },
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.clients.models import Client


@login_required
def welcome_view(request):
    return redirect('client_list')


@login_required
def client_list_view(request):
    clients = Client.objects.all()
    return render(
        request,
        'private/clients/list.html',
        {
            'clients': clients,
            'active_menu': 'clients',
        },
    )

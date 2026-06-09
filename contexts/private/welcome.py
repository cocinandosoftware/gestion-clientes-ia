from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def welcome_view(request):
    return redirect('client_list')

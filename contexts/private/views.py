from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def welcome_view(request):
    return render(request, 'private/welcome.html')

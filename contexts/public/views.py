from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST


def home(request):
    return render(request, 'public/home.html')


@require_http_methods(['GET'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('private_welcome')

    return render(request, 'public/login.html')


@require_POST
def login_validate_view(request):
    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
        login(request, form.get_user())
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('private_welcome'),
        })

    errors = []
    for field_errors in form.errors.values():
        errors.extend(field_errors)

    return JsonResponse({
        'success': False,
        'errors': errors or ['Credenciales incorrectas.'],
    }, status=400)


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

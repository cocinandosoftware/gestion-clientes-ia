from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


def home(request):
    return render(request, 'home.html')


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Iniciar sesión</title>
    </head>
    <body>
        <h1>Iniciar sesión</h1>
        <form method="post">
            {form.as_p()}
            <button type="submit">Entrar</button>
        </form>
        <p><a href="/">Volver al inicio</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('home')

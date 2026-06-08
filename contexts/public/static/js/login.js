document.addEventListener('DOMContentLoaded', function () {
    
    const form = document.getElementById('login-form');
    const errorBox = document.getElementById('login-errors');
    const submitButton = document.getElementById('login-submit');

    if (!form) {
        return;
    }

    form.addEventListener('submit', async function (event) {
        
        event.preventDefault();

        errorBox.hidden = true;
        errorBox.textContent = '';
            submitButton.disabled = true;
            submitButton.classList.add('is-loading');

        try {
            const response = await fetch(form.dataset.validateUrl, {
                method: 'POST',
                body: new FormData(form),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                window.location.href = data.redirect_url;
                return;
            }

            const errors = data.errors || ['No se pudo iniciar sesión.'];
            errorBox.textContent = errors.join(' ');
            errorBox.hidden = false;
        } catch (error) {
            errorBox.textContent = 'Error de conexión. Inténtalo de nuevo.';
            errorBox.hidden = false;
        } finally {
            submitButton.disabled = false;
            submitButton.classList.remove('is-loading');
        }
    });
});

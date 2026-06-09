document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('client-create-form');
    const errorBox = document.getElementById('client-create-errors');
    const submitButton = document.getElementById('client-create-submit');

    if (!form || !errorBox) {
        return;
    }

    const createUrl = form.dataset.createUrl;

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        errorBox.hidden = true;
        errorBox.textContent = '';

        const validationErrors = ClientFormShared.validateForm(form);
        if (validationErrors.length) {
            ClientFormShared.showFormErrors(errorBox, validationErrors);
            return;
        }

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.classList.add('is-loading');
        }

        PrivateLoader.show('Guardando cliente...');

        try {
            const response = await fetch(createUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': ClientFormShared.getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: new FormData(form),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                ClientFormShared.handleWindowSuccess(data.redirect_url);
                return;
            }

            const errors = data.errors || ['No se pudo crear el cliente.'];
            ClientFormShared.showFormErrors(errorBox, errors);
        } catch (error) {
            ClientFormShared.showFormErrors(errorBox, ['Error de conexión. Inténtalo de nuevo.']);
        } finally {
            PrivateLoader.hide();

            if (submitButton) {
                submitButton.disabled = false;
                submitButton.classList.remove('is-loading');
            }
        }
    });
});

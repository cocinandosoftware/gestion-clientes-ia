async function loadClientForEdit(form, errorBox) {
    const detailUrl = form.dataset.detailUrl;

    PrivateLoader.show('Cargando cliente...');

    try {
        const response = await fetch(detailUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        });

        const data = await response.json();

        if (response.ok && data.success) {
            ClientFormShared.populateForm(form, data.client);
            return;
        }

        const errors = data.errors || ['No se pudo cargar el cliente.'];
        ClientFormShared.showFormErrors(errorBox, errors);
    } catch (error) {
        ClientFormShared.showFormErrors(errorBox, ['Error de conexión. Inténtalo de nuevo.']);
    } finally {
        PrivateLoader.hide();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('client-edit-form');
    const errorBox = document.getElementById('client-edit-errors');
    const submitButton = document.getElementById('client-edit-submit');

    if (!form || !errorBox) {
        return;
    }

    const updateUrl = form.dataset.updateUrl;

    loadClientForEdit(form, errorBox);

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

        PrivateLoader.show('Guardando cambios...');

        try {
            const response = await fetch(updateUrl, {
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

            const errors = data.errors || ['No se pudo actualizar el cliente.'];
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

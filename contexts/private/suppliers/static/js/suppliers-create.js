document.addEventListener('DOMContentLoaded', async function () {
    const form = document.getElementById('supplier-create-form');
    const errorBox = document.getElementById('supplier-create-errors');
    const submitButton = document.getElementById('supplier-create-submit');
    const optionsContainer = document.getElementById('supplier-clients-options');

    if (!form || !errorBox) {
        return;
    }

    const createUrl = form.dataset.createUrl;
    const clients = await SupplierFormShared.loadClientOptions(form);
    SupplierFormShared.renderClientOptions(optionsContainer, clients);

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        errorBox.hidden = true;
        errorBox.textContent = '';

        const validationErrors = SupplierFormShared.validateForm(form);
        if (validationErrors.length) {
            SupplierFormShared.showFormErrors(errorBox, validationErrors);
            return;
        }

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.classList.add('is-loading');
        }

        PrivateLoader.show('Guardando proveedor...');

        try {
            const response = await fetch(createUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': SupplierFormShared.getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: new FormData(form),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                SupplierFormShared.handleWindowSuccess(data.redirect_url);
                return;
            }

            const errors = data.errors || ['No se pudo crear el proveedor.'];
            SupplierFormShared.showFormErrors(errorBox, errors);
        } catch (error) {
            SupplierFormShared.showFormErrors(errorBox, ['Error de conexión. Inténtalo de nuevo.']);
        } finally {
            PrivateLoader.hide();

            if (submitButton) {
                submitButton.disabled = false;
                submitButton.classList.remove('is-loading');
            }
        }
    });
});

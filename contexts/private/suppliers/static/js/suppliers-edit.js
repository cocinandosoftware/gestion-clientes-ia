async function loadSupplierForEdit(form, errorBox, optionsContainer) {
    const detailUrl = form.dataset.detailUrl;
    const clients = await SupplierFormShared.loadClientOptions(form, false);

    PrivateLoader.show('Cargando proveedor...');

    try {
        const response = await fetch(detailUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        });

        const data = await response.json();

        if (response.ok && data.success) {
            SupplierFormShared.renderClientOptions(
                optionsContainer,
                clients,
                data.supplier.client_ids || []
            );
            SupplierFormShared.populateForm(form, data.supplier);
            return;
        }

        const errors = data.errors || ['No se pudo cargar el proveedor.'];
        SupplierFormShared.showFormErrors(errorBox, errors);
    } catch (error) {
        SupplierFormShared.showFormErrors(errorBox, ['Error de conexión. Inténtalo de nuevo.']);
    } finally {
        PrivateLoader.hide();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('supplier-edit-form');
    const errorBox = document.getElementById('supplier-edit-errors');
    const submitButton = document.getElementById('supplier-edit-submit');
    const optionsContainer = document.getElementById('supplier-clients-options');

    if (!form || !errorBox) {
        return;
    }

    const updateUrl = form.dataset.updateUrl;

    loadSupplierForEdit(form, errorBox, optionsContainer);

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

        PrivateLoader.show('Guardando cambios...');

        try {
            const response = await fetch(updateUrl, {
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

            const errors = data.errors || ['No se pudo actualizar el proveedor.'];
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

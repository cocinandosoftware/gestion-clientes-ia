const SupplierFormShared = {
    requiredFields: [
        'date',
        'name',
        'company_name',
        'phone',
        'email',
        'address_line',
        'city',
        'postal_code',
        'province',
        'notes',
    ],

    fieldLabels: {
        date: 'fecha',
        name: 'nombre',
        company_name: 'razón social',
        phone: 'teléfono',
        email: 'email',
        address_line: 'dirección',
        city: 'ciudad',
        postal_code: 'código postal',
        province: 'provincia',
        notes: 'notas',
    },

    getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find((row) => row.startsWith('csrftoken='));

        if (!cookieValue) {
            return '';
        }

        return cookieValue.split('=')[1];
    },

    validateForm(form) {
        const errors = [];

        this.requiredFields.forEach((fieldName) => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            const value = field?.value.trim() || '';

            if (!value) {
                errors.push(`El campo ${this.fieldLabels[fieldName]} es obligatorio.`);
            }
        });

        const selectedClients = form.querySelectorAll('input[name="clients"]:checked');
        if (!selectedClients.length) {
            errors.push('Debes seleccionar al menos un cliente asociado.');
        }

        const emailField = form.querySelector('[name="email"]');
        const email = emailField?.value.trim() || '';

        if (email && (!email.includes('@') || !email.split('@')[1]?.includes('.'))) {
            errors.push('El email no es válido.');
        }

        return errors;
    },

    showFormErrors(errorBox, errors) {
        errorBox.textContent = errors.join(' ');
        errorBox.hidden = false;
    },

    populateForm(form, supplier) {
        this.requiredFields.forEach((fieldName) => {
            const field = form.querySelector(`[name="${fieldName}"]`);

            if (field) {
                field.value = supplier[fieldName] || '';
            }
        });

    },

    renderClientOptions(container, clients, selectedIds = []) {
        if (!container) {
            return;
        }

        if (!clients.length) {
            container.innerHTML = '<p class="private-form__empty-options">No hay clientes registrados.</p>';
            return;
        }

        container.innerHTML = clients.map((client) => {
            const checked = selectedIds.includes(client.id) ? ' checked' : '';

            return `
                <label class="private-form__checkbox">
                    <input type="checkbox" name="clients" value="${client.id}"${checked}>
                    <span>${client.name}</span>
                </label>
            `;
        }).join('');
    },

    async loadClientOptions(form, showLoader = true) {
        const optionsUrl = form.dataset.optionsUrl;
        const container = form.querySelector('#supplier-clients-options');

        if (!optionsUrl || !container) {
            return [];
        }

        if (showLoader) {
            PrivateLoader.show('Cargando clientes...');
        }

        try {
            const response = await fetch(optionsUrl, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });

            const data = await response.json();

            if (response.ok && data.success) {
                return data.client_options || [];
            }

            container.innerHTML = '<p class="private-form__empty-options">No se pudieron cargar los clientes.</p>';
            return [];
        } catch (error) {
            container.innerHTML = '<p class="private-form__empty-options">Error de conexión al cargar clientes.</p>';
            return [];
        } finally {
            if (showLoader) {
                PrivateLoader.hide();
            }
        }
    },

    handleWindowSuccess(redirectUrl) {
        const openerWindow = window.opener;

        if (openerWindow && !openerWindow.closed) {
            try {
                if (typeof openerWindow.reloadSupplierList === 'function') {
                    openerWindow.reloadSupplierList();
                } else {
                    openerWindow.location.reload();
                }

                openerWindow.focus();
            } catch (error) {
                openerWindow.location.reload();
            }

            window.close();

            setTimeout(function () {
                if (!window.closed) {
                    window.location.href = redirectUrl;
                }
            }, 500);

            return;
        }

        window.location.href = redirectUrl;
    },
};

window.SupplierFormShared = SupplierFormShared;

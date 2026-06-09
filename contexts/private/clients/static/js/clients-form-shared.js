const ClientFormShared = {
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

    populateForm(form, client) {
        this.requiredFields.forEach((fieldName) => {
            const field = form.querySelector(`[name="${fieldName}"]`);

            if (field) {
                field.value = client[fieldName] || '';
            }
        });
    },

    handleWindowSuccess(redirectUrl) {
        const openerWindow = window.opener;

        if (openerWindow && !openerWindow.closed) {
            try {
                if (typeof openerWindow.reloadClientList === 'function') {
                    openerWindow.reloadClientList();
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

window.ClientFormShared = ClientFormShared;

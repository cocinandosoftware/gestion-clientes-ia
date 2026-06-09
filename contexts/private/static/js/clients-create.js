const REQUIRED_FIELDS = [
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
];

const FIELD_LABELS = {
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
};

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='));

    if (!cookieValue) {
        return '';
    }

    return cookieValue.split('=')[1];
}

function validateClientForm(form) {
    const errors = [];

    REQUIRED_FIELDS.forEach(function (fieldName) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        const value = field?.value.trim() || '';

        if (!value) {
            errors.push(`El campo ${FIELD_LABELS[fieldName]} es obligatorio.`);
        }
    });

    const emailField = form.querySelector('[name="email"]');
    const email = emailField?.value.trim() || '';

    if (email && (!email.includes('@') || !email.split('@')[1]?.includes('.'))) {
        errors.push('El email no es válido.');
    }

    return errors;
}

function showFormErrors(errorBox, errors) {
    errorBox.textContent = errors.join(' ');
    errorBox.hidden = false;
}

function handleCreateSuccess(redirectUrl) {
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
}

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

        const validationErrors = validateClientForm(form);
        if (validationErrors.length) {
            showFormErrors(errorBox, validationErrors);
            return;
        }

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.classList.add('is-loading');
        }

        try {
            const response = await fetch(createUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: new FormData(form),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                handleCreateSuccess(data.redirect_url);
                return;
            }

            const errors = data.errors || ['No se pudo crear el cliente.'];
            showFormErrors(errorBox, errors);
        } catch (error) {
            showFormErrors(errorBox, ['Error de conexión. Inténtalo de nuevo.']);
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.classList.remove('is-loading');
            }
        }
    });
});

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='));

    if (!cookieValue) {
        return '';
    }

    return cookieValue.split('=')[1];
}

function getHasFilters(listSection) {
    return listSection?.dataset.hasFilters === 'true';
}

function showEmptyClientsMessage(hasFilters) {
    const tableWrap = document.getElementById('clients-table-wrap');
    const tbody = document.getElementById('clients-table-body');
    const emptyMessage = document.getElementById('clients-empty');

    if (!tableWrap || !tbody || !emptyMessage) {
        return;
    }

    tableWrap.hidden = true;
    tbody.innerHTML = '';
    emptyMessage.textContent = hasFilters
        ? 'No se encontraron clientes con los filtros aplicados.'
        : 'No hay clientes registrados todavía.';
    emptyMessage.hidden = false;
}

function bindClientDeleteButtons(listSection) {
    const deleteButtons = document.querySelectorAll('.private-btn-delete');
    const hasFilters = getHasFilters(listSection);

    deleteButtons.forEach(function (button) {
        button.addEventListener('click', async function () {
            const clientName = button.dataset.clientName;
            const deleteUrl = button.dataset.deleteUrl;

            if (!confirm(`¿Eliminar a ${clientName}?`)) {
                return;
            }

            button.disabled = true;
            button.classList.add('is-loading');
            PrivateLoader.show('Eliminando cliente...');

            try {
                const response = await fetch(deleteUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    const row = button.closest('tr');
                    const tbody = document.getElementById('clients-table-body');

                    if (row) {
                        row.remove();
                    }

                    if (tbody && !tbody.querySelector('tr')) {
                        showEmptyClientsMessage(hasFilters);
                    }

                    return;
                }

                const errors = data.errors || ['No se pudo eliminar el cliente.'];
                alert(errors.join(' '));
            } catch (error) {
                alert('Error de conexión. Inténtalo de nuevo.');
            } finally {
                PrivateLoader.hide();
                button.disabled = false;
                button.classList.remove('is-loading');
            }
        });
    });
}


function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='));

    if (!cookieValue) {
        return '';
    }

    return cookieValue.split('=')[1];
}

function showEmptyClientsMessage(hasFilters) {
    const tableWrap = document.getElementById('clients-table-wrap');

    if (!tableWrap) {
        return;
    }

    const message = hasFilters
        ? 'No se encontraron clientes con los filtros aplicados.'
        : 'No hay clientes registrados todavía.';

    tableWrap.innerHTML = `<p class="private-empty">${message}</p>`;
}

document.addEventListener('DOMContentLoaded', function () {

    const listSection = document.getElementById('clients-list');
    const deleteButtons = document.querySelectorAll('.private-btn-delete');

    if (!deleteButtons.length) {
        return;
    }



    const hasFilters = listSection?.dataset.hasFilters === 'true';

    deleteButtons.forEach(function (button) {
       
        button.addEventListener('click', async function () {
            const clientName = button.dataset.clientName;
            const deleteUrl = button.dataset.deleteUrl;

            if (!confirm(`¿Eliminar a ${clientName}?`)) {
                return;
            }
            
            console.log("eliminar cliente", clientName);

            button.disabled = true;
            button.classList.add('is-loading');

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
                button.disabled = false;
                button.classList.remove('is-loading');
            }
        });
    });
});

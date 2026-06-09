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

function showEmptySuppliersMessage(hasFilters) {
    const tableWrap = document.getElementById('suppliers-table-wrap');
    const tbody = document.getElementById('suppliers-table-body');
    const emptyMessage = document.getElementById('suppliers-empty');

    if (!tableWrap || !tbody || !emptyMessage) {
        return;
    }

    tableWrap.hidden = true;
    tbody.innerHTML = '';
    emptyMessage.textContent = hasFilters
        ? 'No se encontraron proveedores con los filtros aplicados.'
        : 'No hay proveedores registrados todavía.';
    emptyMessage.hidden = false;
}

function bindSupplierDeleteButtons(listSection) {
    const deleteButtons = document.querySelectorAll('.private-btn-delete');
    const hasFilters = getHasFilters(listSection);

    deleteButtons.forEach(function (button) {
        button.addEventListener('click', async function () {
            const supplierName = button.dataset.supplierName;
            const deleteUrl = button.dataset.deleteUrl;

            if (!confirm(`¿Eliminar a ${supplierName}?`)) {
                return;
            }

            button.disabled = true;
            button.classList.add('is-loading');
            PrivateLoader.show('Eliminando proveedor...');

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
                    const tbody = document.getElementById('suppliers-table-body');

                    if (row) {
                        row.remove();
                    }

                    if (tbody && !tbody.querySelector('tr')) {
                        showEmptySuppliersMessage(hasFilters);
                    }

                    return;
                }

                const errors = data.errors || ['No se pudo eliminar el proveedor.'];
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

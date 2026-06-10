const EDIT_ICON_SVG = `
    <svg
        class="private-btn-edit__icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        aria-hidden="true"
    >
        <path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z"/>
    </svg>
`;

const DELETE_ICON_SVG = `
    <svg
        class="private-btn-delete__icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        aria-hidden="true"
    >
        <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14z"/>
        <path d="M10 11v6M14 11v6"/>
    </svg>
`;

function escapeHtml(value) {
    const element = document.createElement('div');
    element.textContent = value ?? '';
    return element.innerHTML;
}

function renderCell(value, label) {
    if (value) {
        return `<td data-label="${escapeHtml(label)}">${escapeHtml(value)}</td>`;
    }

    return `<td data-label="${escapeHtml(label)}"><span class="private-table__muted">—</span></td>`;
}

function buildClientRow(client) {
    return `
        <tr>
            <td data-label="Nombre">${escapeHtml(client.name)}</td>
            ${renderCell(client.company_name, 'Razón social')}
            ${renderCell(client.email, 'Email')}
            ${renderCell(client.phone, 'Teléfono')}
            ${renderCell(client.city, 'Ciudad')}
            <td data-label="Fecha">${escapeHtml(client.date)}</td>
            <td class="private-table__actions" data-label="Acciones">
                <div class="private-table__actions-inner">
                    <button
                        type="button"
                        class="private-btn-edit"
                        aria-label="Editar ${escapeHtml(client.name)}"
                        data-edit-url="${escapeHtml(client.edit_url)}"
                    >
                        ${EDIT_ICON_SVG}
                    </button>
                    <button
                        type="button"
                        class="private-btn-delete"
                        aria-label="Eliminar ${escapeHtml(client.name)}"
                        data-client-name="${escapeHtml(client.name)}"
                        data-delete-url="${escapeHtml(client.delete_url)}"
                    >
                        ${DELETE_ICON_SVG}
                    </button>
                </div>
            </td>
        </tr>
    `;
}

function setHasFilters(listSection, hasFilters) {
    if (listSection) {
        listSection.dataset.hasFilters = hasFilters ? 'true' : 'false';
    }
}

function showLoadError(message) {
    const emptyMessage = document.getElementById('clients-empty');

    alert(message);

    if (emptyMessage) {
        emptyMessage.textContent = message;
        emptyMessage.hidden = false;
    }
}

function updateClientsView(clients, hasFilters) {
    const tableWrap = document.getElementById('clients-table-wrap');
    const tbody = document.getElementById('clients-table-body');
    const emptyMessage = document.getElementById('clients-empty');
    const listSection = document.getElementById('clients-list');

    if (!tableWrap || !tbody || !emptyMessage) {
        return;
    }

    if (!clients.length) {
        tableWrap.hidden = true;
        emptyMessage.textContent = hasFilters
            ? 'No se encontraron clientes con los filtros aplicados.'
            : 'No hay clientes registrados todavía.';
        emptyMessage.hidden = false;
        tbody.innerHTML = '';
        return;
    }

    tableWrap.hidden = false;
    emptyMessage.hidden = true;
    tbody.innerHTML = clients.map(buildClientRow).join('');
    bindClientEditButtons();
    bindClientDeleteButtons(listSection);
}

function bindClientEditButtons() {
    document.querySelectorAll('.private-btn-edit').forEach(function (button) {
        button.addEventListener('click', function () {
            const editUrl = button.dataset.editUrl;

            if (!editUrl) {
                return;
            }

            window.open(editUrl, '_blank');
        });
    });
}

async function loadClients(listSection, searchForm, searchUrl, submitButton) {
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.classList.add('is-loading');
    }

    PrivateLoader.show('Cargando clientes...');

    try {
        const params = new URLSearchParams(new FormData(searchForm));
        const response = await fetch(`${searchUrl}?${params.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        });

        const data = await response.json();

        if (response.ok && data.success) {
            setHasFilters(listSection, data.has_filters);
            updateClientsView(data.clients, data.has_filters);
            return;
        }

        showLoadError('No se pudieron cargar los clientes.');
    } catch (error) {
        showLoadError('Error de conexión. Inténtalo de nuevo.');
    } finally {
        PrivateLoader.hide();

        if (submitButton) {
            submitButton.disabled = false;
            submitButton.classList.remove('is-loading');
        }
    }
}

function bindClientSearchForm(listSection) {
    const searchForm = document.getElementById('client-search-form');
    const searchUrl = listSection?.dataset.searchUrl;
    const submitButton = document.getElementById('client-search-submit');

    if (!searchForm || !searchUrl) {
        return;
    }

    loadClients(listSection, searchForm, searchUrl, submitButton);

    searchForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        await loadClients(listSection, searchForm, searchUrl, submitButton);
    });
}

function reloadClientList() {
    const listSection = document.getElementById('clients-list');
    const searchForm = document.getElementById('client-search-form');
    const searchUrl = listSection?.dataset.searchUrl;
    const submitButton = document.getElementById('client-search-submit');

    if (!listSection || !searchForm || !searchUrl) {
        return;
    }

    return loadClients(listSection, searchForm, searchUrl, submitButton);
}

window.reloadClientList = reloadClientList;

function bindNewClientButton() {
    const newButton = document.getElementById('client-new-button');

    if (!newButton) {
        return;
    }

    newButton.addEventListener('click', function () {
        const createUrl = newButton.dataset.createUrl;

        if (!createUrl) {
            return;
        }

        window.open(createUrl, '_blank');
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const listSection = document.getElementById('clients-list');
    bindClientSearchForm(listSection);
    bindNewClientButton();
});

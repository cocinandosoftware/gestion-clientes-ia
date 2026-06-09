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

function renderCell(value) {
    if (value) {
        return `<td>${escapeHtml(value)}</td>`;
    }

    return '<td><span class="private-table__muted">—</span></td>';
}

function buildClientRow(client) {
    return `
        <tr>
            <td>${escapeHtml(client.name)}</td>
            ${renderCell(client.company_name)}
            ${renderCell(client.email)}
            ${renderCell(client.phone)}
            ${renderCell(client.city)}
            <td>${escapeHtml(client.date)}</td>
            <td class="private-table__actions">
                <button
                    type="button"
                    class="private-btn-delete"
                    aria-label="Eliminar ${escapeHtml(client.name)}"
                    data-client-name="${escapeHtml(client.name)}"
                    data-delete-url="${escapeHtml(client.delete_url)}"
                >
                    ${DELETE_ICON_SVG}
                </button>
            </td>
        </tr>
    `;
}

function setHasFilters(listSection, hasFilters) {
    if (listSection) {
        listSection.dataset.hasFilters = hasFilters ? 'true' : 'false';
    }
}

function showLoader() {
    const loader = document.getElementById('clients-loader');

    if (!loader) {
        return;
    }

    loader.hidden = false;
    loader.setAttribute('aria-busy', 'true');
    document.body.classList.add('private-loader-active');
}

function hideLoader() {
    const loader = document.getElementById('clients-loader');

    if (!loader) {
        return;
    }

    loader.hidden = true;
    loader.setAttribute('aria-busy', 'false');
    document.body.classList.remove('private-loader-active');
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
    bindClientDeleteButtons(listSection);
}

function syncFormFromUrl(searchForm) {
    const params = new URLSearchParams(window.location.search);

    searchForm.querySelector('[name="q"]').value = params.get('q') || '';
    searchForm.querySelector('[name="date_from"]').value = params.get('date_from') || '';
    searchForm.querySelector('[name="date_until"]').value = params.get('date_until') || '';
}

async function loadClients(listSection, searchForm, searchUrl, submitButton) {
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.classList.add('is-loading');
    }

    showLoader();

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
        hideLoader();

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

    syncFormFromUrl(searchForm);
    loadClients(listSection, searchForm, searchUrl, submitButton);

    searchForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        await loadClients(listSection, searchForm, searchUrl, submitButton);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const listSection = document.getElementById('clients-list');
    bindClientSearchForm(listSection);
});

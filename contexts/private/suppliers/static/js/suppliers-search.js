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

function renderClientsCell(supplier) {
    const label = supplier.clients_label;

    if (!label) {
        return `<td class="private-table__cell--clients" data-label="Clientes"><span class="private-table__muted">—</span></td>`;
    }

    const tooltip = supplier.clients_tooltip || '';

    if (!tooltip) {
        return `
            <td class="private-table__cell--clients" data-label="Clientes">
                <span class="private-tooltip">
                    <span class="private-tooltip__trigger private-tooltip__trigger--static">${escapeHtml(label)}</span>
                </span>
            </td>
        `;
    }

    return `
        <td class="private-table__cell--clients" data-label="Clientes">
            <span class="private-tooltip private-tooltip--interactive" data-private-tooltip>
                <button type="button" class="private-tooltip__trigger">${escapeHtml(label)}</button>
                <div class="private-tooltip__panel" hidden role="tooltip">
                    <span class="private-tooltip__title">Clientes asociados</span>
                    <span class="private-tooltip__text">${escapeHtml(tooltip)}</span>
                </div>
            </span>
        </td>
    `;
}

function buildSupplierRow(supplier) {
    return `
        <tr>
            <td data-label="Nombre">${escapeHtml(supplier.name)}</td>
            ${renderCell(supplier.company_name, 'Razón social')}
            ${renderCell(supplier.email, 'Email')}
            ${renderCell(supplier.phone, 'Teléfono')}
            ${renderCell(supplier.city, 'Ciudad')}
            ${renderClientsCell(supplier)}
            <td data-label="Fecha">${escapeHtml(supplier.date)}</td>
            <td class="private-table__actions" data-label="Acciones">
                <div class="private-table__actions-inner">
                    <button
                        type="button"
                        class="private-btn-edit"
                        aria-label="Editar ${escapeHtml(supplier.name)}"
                        data-edit-url="${escapeHtml(supplier.edit_url)}"
                    >
                        ${EDIT_ICON_SVG}
                    </button>
                    <button
                        type="button"
                        class="private-btn-delete"
                        aria-label="Eliminar ${escapeHtml(supplier.name)}"
                        data-supplier-name="${escapeHtml(supplier.name)}"
                        data-delete-url="${escapeHtml(supplier.delete_url)}"
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
    const emptyMessage = document.getElementById('suppliers-empty');

    alert(message);

    if (emptyMessage) {
        emptyMessage.textContent = message;
        emptyMessage.hidden = false;
    }
}

function populateClientFilter(select, clientOptions, selectedValue) {
    if (!select) {
        return;
    }

    const currentValue = selectedValue || select.value || '';
    const optionsHtml = clientOptions.map((client) => {
        const selected = String(client.id) === String(currentValue) ? ' selected' : '';

        return `<option value="${client.id}"${selected}>${escapeHtml(client.name)}</option>`;
    }).join('');

    select.innerHTML = `<option value="">Todos los clientes</option>${optionsHtml}`;
}

function updateSuppliersView(suppliers, hasFilters, pagination, sort, searchForm) {
    const tableWrap = document.getElementById('suppliers-table-wrap');
    const tbody = document.getElementById('suppliers-table-body');
    const emptyMessage = document.getElementById('suppliers-empty');
    const listSection = document.getElementById('suppliers-list');
    const paginationEl = document.getElementById('suppliers-pagination');

    if (!tableWrap || !tbody || !emptyMessage) {
        return;
    }

    if (!suppliers.length) {
        tableWrap.hidden = true;
        if (paginationEl) {
            paginationEl.hidden = true;
        }
        emptyMessage.textContent = hasFilters
            ? 'No se encontraron proveedores con los filtros aplicados.'
            : 'No hay proveedores registrados todavía.';
        emptyMessage.hidden = false;
        tbody.innerHTML = '';
        return;
    }

    tableWrap.hidden = false;
    emptyMessage.hidden = true;
    tbody.innerHTML = suppliers.map(buildSupplierRow).join('');
    bindSupplierEditButtons();
    bindSupplierDeleteButtons(listSection);
    PrivateTooltip.bind(tbody);

    if (searchForm && pagination) {
        const pageInput = searchForm.querySelector('[name="page"]');

        if (pageInput) {
            pageInput.value = String(pagination.page);
        }
    }

    PrivateListing.updatePaginationView({
        paginationId: 'suppliers-pagination',
        infoId: 'suppliers-pagination-info',
        prevId: 'suppliers-pagination-prev',
        nextId: 'suppliers-pagination-next',
        pagesId: 'suppliers-pagination-pages',
        pageSizeSelectId: 'suppliers-page-size',
        form: searchForm,
        pagination,
    });

    if (sort) {
        PrivateListing.updateSortIndicators('#suppliers-table', sort.field, sort.order);
    }
}

function bindSupplierEditButtons() {
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

async function loadSuppliers(listSection, searchForm, searchUrl, submitButton) {
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.classList.add('is-loading');
    }

    PrivateLoader.show('Cargando proveedores...');

    try {
        const params = new URLSearchParams(new FormData(searchForm));
        const response = await fetch(`${searchUrl}?${params.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        });

        const data = await response.json();

        if (response.ok && data.success) {
            const clientSelect = searchForm.querySelector('[name="client_id"]');
            populateClientFilter(clientSelect, data.client_options || [], clientSelect?.value);

            setHasFilters(listSection, data.has_filters);
            updateSuppliersView(
                data.suppliers,
                data.has_filters,
                data.pagination,
                data.sort,
                searchForm
            );
            return;
        }

        showLoadError('No se pudieron cargar los proveedores.');
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

function bindSupplierSearchForm(listSection) {
    const searchForm = document.getElementById('supplier-search-form');
    const searchUrl = listSection?.dataset.searchUrl;
    const submitButton = document.getElementById('supplier-search-submit');

    if (!searchForm || !searchUrl) {
        return;
    }

    const reload = () => loadSuppliers(listSection, searchForm, searchUrl, submitButton);

    PrivateListing.bindSortableHeaders({
        tableSelector: '#suppliers-table',
        form: searchForm,
        onSortChange: reload,
    });

    PrivateListing.bindPagination({
        paginationId: 'suppliers-pagination',
        infoId: 'suppliers-pagination-info',
        prevId: 'suppliers-pagination-prev',
        nextId: 'suppliers-pagination-next',
        pagesId: 'suppliers-pagination-pages',
        pageSizeSelectId: 'suppliers-page-size',
        form: searchForm,
        onPageChange: reload,
    });

    reload();

    searchForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        PrivateListing.resetPage(searchForm);
        await reload();
    });
}

function reloadSupplierList() {
    const listSection = document.getElementById('suppliers-list');
    const searchForm = document.getElementById('supplier-search-form');
    const searchUrl = listSection?.dataset.searchUrl;
    const submitButton = document.getElementById('supplier-search-submit');

    if (!listSection || !searchForm || !searchUrl) {
        return;
    }

    return loadSuppliers(listSection, searchForm, searchUrl, submitButton);
}

window.reloadSupplierList = reloadSupplierList;

function bindNewSupplierButton() {
    const newButton = document.getElementById('supplier-new-button');

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
    const listSection = document.getElementById('suppliers-list');
    bindSupplierSearchForm(listSection);
    bindNewSupplierButton();
});

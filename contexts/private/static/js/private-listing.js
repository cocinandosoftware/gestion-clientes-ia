const PrivateListing = {
    DEFAULT_PAGE_SIZE: 20,

    resetPage(form) {
        const pageInput = form.querySelector('[name="page"]');

        if (pageInput) {
            pageInput.value = '1';
        }
    },

    updateSortIndicators(tableSelector, sortField, sortOrder) {
        document.querySelectorAll(`${tableSelector} [data-sort-field]`).forEach((headerCell) => {
            const button = headerCell.querySelector('.private-table__sort');
            const field = headerCell.dataset.sortField;

            if (!button) {
                return;
            }

            button.classList.remove(
                'private-table__sort--active',
                'private-table__sort--asc',
                'private-table__sort--desc'
            );

            if (field === sortField) {
                button.classList.add('private-table__sort--active', `private-table__sort--${sortOrder}`);
            }
        });
    },

    bindSortableHeaders(config) {
        const { tableSelector, form, onSortChange } = config;
        const table = document.querySelector(tableSelector);

        if (!table || !form) {
            return;
        }

        const sortInput = form.querySelector('[name="sort"]');
        const orderInput = form.querySelector('[name="order"]');

        if (!sortInput || !orderInput) {
            return;
        }

        table.querySelectorAll('[data-sort-field] .private-table__sort').forEach((button) => {
            button.addEventListener('click', function () {
                const headerCell = button.closest('[data-sort-field]');
                const field = headerCell?.dataset.sortField;

                if (!field) {
                    return;
                }

                let newOrder = 'asc';

                if (sortInput.value === field && orderInput.value === 'asc') {
                    newOrder = 'desc';
                }

                sortInput.value = field;
                orderInput.value = newOrder;
                PrivateListing.resetPage(form);
                PrivateListing.updateSortIndicators(tableSelector, field, newOrder);
                onSortChange();
            });
        });

        PrivateListing.updateSortIndicators(tableSelector, sortInput.value, orderInput.value);
    },

    syncPageSize(pageSizeSelectId, form, pageSize) {
        const select = document.getElementById(pageSizeSelectId);
        const pageSizeInput = form?.querySelector('[name="page_size"]');
        const value = String(pageSize);

        if (select && select.value !== value) {
            select.value = value;
        }

        if (pageSizeInput && pageSizeInput.value !== value) {
            pageSizeInput.value = value;
        }
    },

    buildPageItems(currentPage, totalPages) {
        if (totalPages <= 1) {
            return [1];
        }

        if (totalPages <= 7) {
            return Array.from({ length: totalPages }, (_, index) => index + 1);
        }

        const pages = [];
        let start = Math.max(2, currentPage - 1);
        let end = Math.min(totalPages - 1, currentPage + 1);

        if (currentPage <= 3) {
            start = 2;
            end = 4;
        } else if (currentPage >= totalPages - 2) {
            start = totalPages - 3;
            end = totalPages - 1;
        }

        pages.push(1);

        if (start > 2) {
            pages.push('ellipsis');
        }

        for (let page = start; page <= end; page += 1) {
            pages.push(page);
        }

        if (end < totalPages - 1) {
            pages.push('ellipsis');
        }

        pages.push(totalPages);

        return pages;
    },

    renderPageButtons(pagesId, currentPage, totalPages) {
        const container = document.getElementById(pagesId);

        if (!container) {
            return;
        }

        const items = PrivateListing.buildPageItems(currentPage, totalPages);

        container.innerHTML = items.map((item) => {
            if (item === 'ellipsis') {
                return '<span class="private-pagination__ellipsis" aria-hidden="true">…</span>';
            }

            const isActive = item === currentPage;

            return `
                <button
                    type="button"
                    class="private-pagination__page${isActive ? ' is-active' : ''}"
                    data-page="${item}"
                    ${isActive ? 'aria-current="page"' : ''}
                    aria-label="Página ${item}"
                >${item}</button>
            `;
        }).join('');
    },

    bindPagination(config) {
        const {
            paginationId,
            infoId,
            prevId,
            nextId,
            pagesId,
            pageSizeSelectId,
            form,
            onPageChange,
        } = config;
        const pagination = document.getElementById(paginationId);
        const info = document.getElementById(infoId);
        const prevButton = document.getElementById(prevId);
        const nextButton = document.getElementById(nextId);
        const pagesContainer = pagesId ? document.getElementById(pagesId) : null;
        const pageSizeSelect = pageSizeSelectId
            ? document.getElementById(pageSizeSelectId)
            : null;
        const pageInput = form?.querySelector('[name="page"]');
        const pageSizeInput = form?.querySelector('[name="page_size"]');

        if (!pagination || !info || !prevButton || !nextButton || !pageInput) {
            return;
        }

        if (pageSizeSelect && pageSizeInput) {
            pageSizeSelect.addEventListener('change', function () {
                pageSizeInput.value = pageSizeSelect.value;
                PrivateListing.resetPage(form);
                onPageChange();
            });
        }

        if (pagesContainer) {
            pagesContainer.addEventListener('click', function (event) {
                const button = event.target.closest('[data-page]');

                if (!button || button.classList.contains('is-active')) {
                    return;
                }

                pageInput.value = button.dataset.page;
                onPageChange();
            });
        }

        prevButton.addEventListener('click', function () {
            const currentPage = Number(pageInput.value || 1);

            if (currentPage <= 1) {
                return;
            }

            pageInput.value = String(currentPage - 1);
            onPageChange();
        });

        nextButton.addEventListener('click', function () {
            const currentPage = Number(pageInput.value || 1);
            pageInput.value = String(currentPage + 1);
            onPageChange();
        });
    },

    updatePaginationView(config) {
        const {
            paginationId,
            infoId,
            prevId,
            nextId,
            pagesId,
            pageSizeSelectId,
            form,
            pagination,
        } = config;
        const paginationEl = document.getElementById(paginationId);
        const info = document.getElementById(infoId);
        const prevButton = document.getElementById(prevId);
        const nextButton = document.getElementById(nextId);

        if (!paginationEl || !info || !prevButton || !nextButton || !pagination) {
            return;
        }

        if (!pagination.total_count) {
            paginationEl.hidden = true;
            return;
        }

        paginationEl.hidden = false;
        info.textContent = `${pagination.total_count} registros · página ${pagination.page} de ${pagination.total_pages}`;
        prevButton.disabled = !pagination.has_previous;
        nextButton.disabled = !pagination.has_next;

        if (pagesId) {
            PrivateListing.renderPageButtons(pagesId, pagination.page, pagination.total_pages);
        }

        if (pageSizeSelectId && form && pagination.page_size) {
            PrivateListing.syncPageSize(pageSizeSelectId, form, pagination.page_size);
        }
    },

};

window.PrivateListing = PrivateListing;

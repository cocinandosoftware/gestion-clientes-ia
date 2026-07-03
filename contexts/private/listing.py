DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


CLIENT_SORT_FIELDS = {
    'id': 'id',
    'name': 'name',
    'company_name': 'company_name',
    'email': 'email',
    'phone': 'phone',
    'city': 'city',
    'date': 'date',
}

SUPPLIER_SORT_FIELDS = {
    'name': 'name',
    'company_name': 'company_name',
    'email': 'email',
    'phone': 'phone',
    'city': 'city',
    'date': 'date',
}


def parse_page(value, default=1):
    try:
        page = int(value)
    except (TypeError, ValueError):
        return default

    return max(1, page)


def parse_page_size(value, default=DEFAULT_PAGE_SIZE):
    try:
        page_size = int(value)
    except (TypeError, ValueError):
        return default

    return min(max(1, page_size), MAX_PAGE_SIZE)


def parse_sort_field(value, allowed_fields, default):
    if value in allowed_fields:
        return value

    return default


def parse_sort_order(value, default='asc'):
    if value in ('asc', 'desc'):
        return value

    return default


def build_order_by(sort_field, sort_order, field_map):
    db_field = field_map[sort_field]
    prefix = '-' if sort_order == 'desc' else ''

    return f'{prefix}{db_field}'


def build_pagination_meta(total_count, page, page_size):
    if total_count == 0:
        return {
            'page': 1,
            'page_size': page_size,
            'total_count': 0,
            'total_pages': 1,
            'has_previous': False,
            'has_next': False,
        }

    total_pages = (total_count + page_size - 1) // page_size
    page = min(page, total_pages)

    return {
        'page': page,
        'page_size': page_size,
        'total_count': total_count,
        'total_pages': total_pages,
        'has_previous': page > 1,
        'has_next': page < total_pages,
    }


def paginate_queryset(queryset, page, page_size):
    total_count = queryset.count()
    pagination = build_pagination_meta(total_count, page, page_size)
    start = (pagination['page'] - 1) * page_size
    items = list(queryset[start:start + page_size])

    return items, pagination


def parse_list_request_params(request, sort_fields, default_sort='name', default_order='asc'):
    page = parse_page(request.GET.get('page', 1))
    page_size = parse_page_size(request.GET.get('page_size', DEFAULT_PAGE_SIZE))
    sort_field = parse_sort_field(
        request.GET.get('sort', '').strip(),
        sort_fields,
        default_sort,
    )
    sort_order = parse_sort_order(request.GET.get('order', '').strip(), default_order)
    order_by = build_order_by(sort_field, sort_order, sort_fields)

    return {
        'page': page,
        'page_size': page_size,
        'sort_field': sort_field,
        'sort_order': sort_order,
        'order_by': order_by,
    }

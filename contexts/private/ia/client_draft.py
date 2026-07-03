from contexts.private.clients.validation import CLIENT_FIELD_LABELS, REQUIRED_CLIENT_FIELDS

SESSION_DRAFT_KEY = 'ia_client_create_draft'


def empty_client_create_draft():
    return {field: '' for field in REQUIRED_CLIENT_FIELDS}


def get_client_create_draft(session):
    if session is None:
        return empty_client_create_draft()

    draft = session.get(SESSION_DRAFT_KEY)
    if not isinstance(draft, dict):
        return empty_client_create_draft()

    return {
        field: str(draft.get(field, '')).strip()
        for field in REQUIRED_CLIENT_FIELDS
    }


def save_client_create_draft(session, draft):
    if session is None:
        return

    session[SESSION_DRAFT_KEY] = draft
    session.modified = True


def clear_client_create_draft(session):
    if session is None:
        return

    if SESSION_DRAFT_KEY in session:
        del session[SESSION_DRAFT_KEY]
        session.modified = True


def merge_client_create_draft(session, partial_fields):
    draft = get_client_create_draft(session)

    for field, value in partial_fields.items():
        if value:
            draft[field] = value

    save_client_create_draft(session, draft)
    return draft

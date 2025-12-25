from sessions import user_sessions


def get_auth_headers(telegram_user_id: int) -> dict | None:
    token = user_sessions.get(telegram_user_id)

    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}"
    }

# Simple in-memory session storage.
# Maps Telegram user IDs to JWT access tokens.

user_sessions: dict[int, str] = {}

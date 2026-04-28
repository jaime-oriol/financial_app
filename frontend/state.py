"""Helpers de sesion: lee/escribe el JWT en app.storage.user (cookie + server side).
Persiste entre navegaciones de pagina y reinicios del navegador.
"""

from nicegui import app


def get_token() -> str | None:
    return app.storage.user.get("token")


def get_user_id() -> int | None:
    return app.storage.user.get("user_id")


def set_auth(token: str, user_id: int) -> None:
    app.storage.user["token"] = token
    app.storage.user["user_id"] = user_id


def clear_auth() -> None:
    app.storage.user.pop("token", None)
    app.storage.user.pop("user_id", None)


def is_authenticated() -> bool:
    return get_token() is not None

"""App shell: container mobile-first centrado + bottom nav fija.
Usar en cada page como context manager: `with app_shell(active='/'): ...`.
Tambien expone helpers comunes (header, section, card) para que las pages
queden cortas y consistentes.
"""

from contextlib import contextmanager
from typing import Iterator

from nicegui import ui

import state
import theme

# Tabs del bottom nav. Si quieres anadir una nueva, solo edita aqui.
NAV_ITEMS: list[tuple[str, str, str]] = [
    ("home", "Home", "/"),
    ("account_balance_wallet", "Budget", "/budget"),
    ("emoji_events", "Challenges", "/challenges"),
    ("flag", "Goals", "/goals"),
    ("person", "Profile", "/profile"),
]


def page_setup(title: str = "FAPP") -> None:
    """CSS global, viewport mobile, fuente y fondo. Llamar al inicio de cada page."""
    ui.page_title(title)
    ui.add_head_html(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, '
        'maximum-scale=1.0, user-scalable=no">'
    )
    ui.add_head_html(
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;'
        '600;700;800;900&display=swap" rel="stylesheet">'
    )
    ui.add_css(
        f"""
        body {{
            background-color: {theme.BG};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: {theme.PRIMARY};
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            -webkit-tap-highlight-color: transparent;
            overscroll-behavior-y: contain;
        }}
        .nicegui-content {{ padding: 0; }}
        @keyframes fapp-fade-in {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .nicegui-content > * {{ animation: fapp-fade-in 0.28s ease-out; }}
        .fapp-card {{
            background: {theme.WHITE};
            border-radius: 20px;
            border: 1px solid rgba(0,0,0,0.055);
            box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 6px 20px rgba(0,0,0,0.05);
            padding: 18px;
            transition: box-shadow 0.2s ease, transform 0.2s ease;
        }}
        .fapp-card:hover {{
            box-shadow: 0 4px 28px rgba(0,0,0,0.10);
            transform: translateY(-1px);
        }}
        .fapp-stat-num {{
            font-size: 26px;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -0.5px;
            font-variant-numeric: tabular-nums;
        }}
        .fapp-money {{ font-variant-numeric: tabular-nums; letter-spacing: -0.2px; }}
        .fapp-section-label {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.4px;
            color: {theme.GREY_TEXT};
            text-transform: uppercase;
        }}
        .fapp-page-title {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.6px;
            color: {theme.PRIMARY};
            line-height: 1.1;
        }}
        .fapp-page-subtitle {{
            font-size: 13px;
            color: {theme.GREY_TEXT};
            font-weight: 400;
            margin-top: 2px;
        }}
        html {{ scroll-behavior: smooth; }}
        .q-btn:active:not(.disabled) {{ transform: scale(0.97); transition: transform 0.1s; }}
        .q-notification {{
            border-radius: 14px !important;
            font-weight: 600 !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.14) !important;
        }}
        .q-field--outlined .q-field__control {{ border-radius: 14px !important; }}
        .q-field--outlined .q-field__control:before {{
            border-color: #E4E8EE !important;
            border-width: 1.5px !important;
        }}
        .q-field--outlined.q-field--focused .q-field__control:before {{
            border-color: {theme.SECONDARY} !important;
            border-width: 2px !important;
        }}
        .q-field__label {{ font-weight: 500 !important; }}
        .q-dialog__backdrop {{
            backdrop-filter: blur(6px) !important;
            -webkit-backdrop-filter: blur(6px) !important;
            background: rgba(10,18,40,0.5) !important;
        }}
        .q-card {{ border-radius: 22px !important; }}
        ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
        ::-webkit-scrollbar-thumb {{ background: {theme.GREY_SOFT}66; border-radius: 2px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        .q-linear-progress, .q-linear-progress__track {{ border-radius: 99px !important; }}
        """
    )


def require_auth() -> bool:
    """Redirigir a /login si no hay token. Usar al inicio de pages protegidas."""
    if not state.is_authenticated():
        ui.navigate.to("/login")
        return False
    return True


@contextmanager
def app_shell(active: str | None = None) -> Iterator[None]:
    """Wrap a page in the standard mobile-app shell.
    active: ruta del tab activo (para resaltar el icono).
    """
    page_setup()

    # Contenedor principal (mobile-first, centrado en desktop)
    with ui.column().classes(
        "w-full max-w-[480px] mx-auto pb-24 min-h-screen gap-0"
    ).style(f"background-color: {theme.BG};"):
        yield

    # Bottom navigation (q-footer = fijo)
    with ui.footer().classes("q-py-none").style(
        f"background-color: {theme.WHITE}; "
        "box-shadow: 0 -1px 0 rgba(0,0,0,0.06), 0 -8px 24px rgba(0,0,0,0.05);"
    ):
        with ui.row().classes(
            "w-full max-w-[480px] mx-auto justify-around items-center"
        ).style("padding: 4px 4px 8px 4px;"):
            for icon, label, path in NAV_ITEMS:
                _nav_item(icon, label, path, is_active=(active == path))


def _nav_item(icon: str, label: str, path: str, is_active: bool) -> None:
    color = theme.SECONDARY if is_active else "#8E9BAA"
    weight = "700" if is_active else "500"
    icon_bg = f"{theme.SECONDARY}18" if is_active else "transparent"
    with ui.column().classes("items-center cursor-pointer gap-0").style(
        "padding: 4px 6px 4px 6px; min-width: 60px;"
    ).on("click", lambda: ui.navigate.to(path)):
        with ui.element("div").style(
            f"background: {icon_bg}; border-radius: 14px; padding: 4px 16px; "
            "transition: background 0.2s ease; margin-bottom: 2px;"
        ):
            ui.icon(icon).style(f"color: {color}; font-size: 22px;")
        ui.label(label).style(
            f"color: {color}; font-size: 10px; font-weight: {weight};"
        )


# --- Helpers de UI reutilizables ---

@contextmanager
def section(title: str | None = None, padding_x: int = 16, top: int = 18) -> Iterator[None]:
    """Bloque vertical con label opcional en mayusculas (estilo wireframe)."""
    with ui.column().classes("w-full gap-2").style(
        f"padding: {top}px {padding_x}px 0 {padding_x}px;"
    ):
        if title:
            ui.label(title).classes("fapp-section-label")
        yield


@contextmanager
def card(padding: int = 18) -> Iterator[None]:
    with ui.column().classes("w-full gap-2").style(
        f"background: {theme.WHITE}; border-radius: 20px; "
        "box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 6px 20px rgba(0,0,0,0.05); "
        f"padding: {padding}px;"
    ):
        yield


def render_avatar(container, user: dict, size: int = 64, font_size: int = 28) -> None:
    """Renderiza el avatar del usuario en `container` (lo limpia primero).
    - Si tiene foto (data URL): la pinta circular con object-fit cover.
    - Si no: circulo de color estable por user_id con la inicial del nombre.
    """
    container.clear()
    with container:
        avatar = user.get("avatar")
        if avatar and avatar.startswith("data:"):
            ui.image(avatar).style(
                f"width: {size}px; height: {size}px; border-radius: 50%; "
                "object-fit: cover; display: block;"
            )
        else:
            color = theme.avatar_color(user.get("user_id", 0))
            initial = (user.get("name") or "?")[0].upper()
            with ui.element("div").style(
                f"width: {size}px; height: {size}px; border-radius: 50%; "
                f"background: {color}; display: flex; align-items: center; "
                "justify-content: center;"
            ):
                ui.label(initial).style(
                    f"color: white; font-size: {font_size}px; font-weight: 700; "
                    "line-height: 1;"
                )


def empty_state(icon: str, message: str, subtitle: str | None = None) -> None:
    """Estado vacio para listas sin datos."""
    with ui.column().classes("w-full items-center gap-2").style("padding: 32px 16px;"):
        with ui.element("div").style(
            f"background: {theme.GREY_BG}; width: 56px; height: 56px; border-radius: 16px; "
            "display: flex; align-items: center; justify-content: center;"
        ):
            ui.icon(icon).style(f"color: {theme.GREY_SOFT}; font-size: 26px;")
        ui.label(message).style(
            f"color: {theme.PRIMARY}; font-size: 14px; font-weight: 600; text-align: center;"
        )
        if subtitle:
            ui.label(subtitle).style(
                f"color: {theme.GREY_TEXT}; font-size: 12px; text-align: center; max-width: 260px;"
            )


def primary_button(text: str, on_click, icon: str | None = None) -> ui.button:
    btn = ui.button(text, icon=icon, on_click=on_click).props(
        "unelevated rounded no-caps"
    ).classes("w-full").style(
        f"background-color: {theme.SECONDARY}; color: {theme.WHITE}; "
        "height: 48px; font-weight: 600; font-size: 14px; letter-spacing: 0.2px;"
    )
    return btn


def outlined_button(text: str, on_click, icon: str | None = None) -> ui.button:
    btn = ui.button(text, icon=icon, on_click=on_click).props(
        "outline rounded no-caps"
    ).classes("w-full").style(
        f"color: {theme.SECONDARY}; height: 48px; font-weight: 600; "
        f"border-color: {theme.SECONDARY}; font-size: 14px; letter-spacing: 0.2px;"
    )
    return btn

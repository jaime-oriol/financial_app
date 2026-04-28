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
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;'
        '600;700;800&display=swap" rel="stylesheet">'
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
        .nicegui-content {{
            padding: 0;
        }}
        /* Fade-in suave al cargar (sensacion premium) */
        @keyframes fapp-fade-in {{
            from {{ opacity: 0; transform: translateY(4px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .nicegui-content > * {{
            animation: fapp-fade-in 0.28s ease-out;
        }}
        .fapp-card {{
            background: {theme.WHITE};
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            padding: 18px;
            transition: box-shadow 0.18s ease, transform 0.18s ease;
        }}
        .fapp-card:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.07);
        }}
        .fapp-stat-num {{
            font-size: 28px;
            font-weight: 800;
            line-height: 1;
            font-variant-numeric: tabular-nums;
        }}
        .fapp-money {{
            font-variant-numeric: tabular-nums;
        }}
        .fapp-section-label {{
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            color: {theme.GREY_TEXT};
            text-transform: uppercase;
        }}
        html {{ scroll-behavior: smooth; }}
        /* Tap feedback en botones */
        .q-btn:active:not(.disabled) {{
            transform: scale(0.97);
        }}
        /* Notifications mas pulidas */
        .q-notification {{
            border-radius: 12px !important;
            font-weight: 500 !important;
        }}
        /* Scrollbar fino y discreto */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-thumb {{
            background: {theme.GREY_SOFT}aa; border-radius: 3px;
        }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
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
        f"background-color: {theme.WHITE}; border-top: 1px solid {theme.GREY_BG}; "
        "box-shadow: 0 -2px 10px rgba(0,0,0,0.04);"
    ):
        with ui.row().classes(
            "w-full max-w-[480px] mx-auto justify-around items-center"
        ).style("padding: 6px 4px;"):
            for icon, label, path in NAV_ITEMS:
                _nav_item(icon, label, path, is_active=(active == path))


def _nav_item(icon: str, label: str, path: str, is_active: bool) -> None:
    color = theme.SECONDARY if is_active else theme.GREY_SOFT
    weight = "700" if is_active else "500"
    with ui.column().classes("items-center cursor-pointer gap-0").style(
        "padding: 6px 8px; min-width: 56px; transition: transform 0.15s ease;"
    ).on("click", lambda: ui.navigate.to(path)):
        ui.icon(icon).style(f"color: {color}; font-size: 24px;")
        ui.label(label).style(
            f"color: {color}; font-size: 10.5px; font-weight: {weight};"
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
        f"background: {theme.WHITE}; border-radius: 16px; "
        f"box-shadow: 0 2px 8px rgba(0,0,0,0.04); padding: {padding}px;"
    ):
        yield


def empty_state(icon: str, message: str) -> None:
    """Estado vacio bonito para reemplazar listas sin datos."""
    with ui.column().classes("w-full items-center gap-2").style("padding: 32px 16px;"):
        ui.icon(icon).style(f"color: {theme.GREY_SOFT}; font-size: 48px;")
        ui.label(message).style(
            f"color: {theme.GREY_TEXT}; font-size: 13px; text-align: center;"
        )


def primary_button(text: str, on_click, icon: str | None = None) -> ui.button:
    btn = ui.button(text, icon=icon, on_click=on_click).props(
        "unelevated rounded no-caps"
    ).classes("w-full").style(
        f"background-color: {theme.SECONDARY}; color: {theme.WHITE}; "
        "height: 48px; font-weight: 600;"
    )
    return btn


def outlined_button(text: str, on_click, icon: str | None = None) -> ui.button:
    btn = ui.button(text, icon=icon, on_click=on_click).props(
        "outline rounded no-caps"
    ).classes("w-full").style(
        f"color: {theme.SECONDARY}; height: 48px; font-weight: 600; "
        f"border-color: {theme.SECONDARY};"
    )
    return btn

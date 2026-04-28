"""Diálogos transaccionales reutilizables (add expense, create budget, contribute,
create goal, confirm). Cada uno acepta un on_success async callback para que la
page que lo invoca refresque sus datos sin acoplamiento.

Categorías cacheadas en memoria: son seeds del backend, no cambian — evitamos
una llamada HTTP cada vez que se abre un diálogo.
"""

from datetime import date
from typing import Awaitable, Callable

from nicegui import ui

import api
import theme

OnSuccess = Callable[[], Awaitable[None]] | None


_categories_cache: list[dict] | None = None


async def get_categories() -> list[dict]:
    global _categories_cache
    if _categories_cache is None:
        _categories_cache = await api.get_categories()
    return _categories_cache


# --- Helpers internos ---

def _dialog_card():
    return ui.card().style(
        f"width: 360px; max-width: 92vw; border-radius: 18px; padding: 22px; "
        f"background: {theme.WHITE};"
    )


def _dialog_title(text: str) -> None:
    ui.label(text).style(
        f"color: {theme.PRIMARY}; font-size: 18px; font-weight: 700; margin-bottom: 6px;"
    )


def _category_chip_group(categories: list[dict]) -> dict:
    """Chips de categoria con seleccion unica. Visual claro: el seleccionado
    pinta del color de su categoria (relleno solido) con icono y texto blancos;
    los no-seleccionados quedan en gris suave. Usamos `flat` + style con
    !important para anular los defaults de Quasar (que pintaria todos azul).
    """
    state = {"selected_id": None}
    chips_data: list[tuple[int, "ui.button", str]] = []

    def repaint() -> None:
        for cat_id, chip, color in chips_data:
            is_sel = cat_id == state["selected_id"]
            if is_sel:
                chip.style(
                    f"background: {color} !important; color: white !important; "
                    f"font-weight: 700; box-shadow: 0 2px 8px {color}66; "
                    "transform: scale(1.02); transition: all 0.15s ease;"
                )
            else:
                chip.style(
                    f"background: {theme.GREY_BG} !important; "
                    f"color: {theme.GREY_TEXT} !important; "
                    "font-weight: 500; box-shadow: none; transform: scale(1); "
                    "transition: all 0.15s ease;"
                )

    with ui.row().classes("w-full gap-2 flex-wrap"):
        for cat in categories:
            color = theme.category_color(cat["category_id"])
            chip = ui.button(
                cat["name"], icon=theme.category_icon(cat["category_id"])
            ).props("dense no-caps rounded flat")
            chips_data.append((cat["category_id"], chip, color))

            def make_handler(cid: int = cat["category_id"]):
                def handler() -> None:
                    state["selected_id"] = cid
                    repaint()
                return handler

            chip.on("click", make_handler())

    repaint()
    return state


def _date_input(label: str, default: str | None = None):
    """Input de fecha con date picker en popup."""
    inp = ui.input(label, value=default or "").props(
        "outlined dense readonly clearable"
    ).classes("w-full")
    with inp.add_slot("append"):
        ui.icon("event").classes("cursor-pointer").on(
            "click", lambda: picker_dialog.open()
        )
    with ui.dialog() as picker_dialog, ui.card():
        ui.date(
            value=default or date.today().isoformat(),
            on_change=lambda e: setattr(inp, "value", e.value or ""),
        ).props("mask=YYYY-MM-DD")
        ui.button("OK", on_click=picker_dialog.close).props("flat")
    return inp


def _dialog_actions(dialog: "ui.dialog", primary_text: str, on_primary,
                    primary_color: str = theme.SECONDARY) -> None:
    with ui.row().classes("w-full justify-end gap-2").style("margin-top: 14px;"):
        ui.button("Cancel", on_click=dialog.close).props("flat no-caps").style(
            f"color: {theme.GREY_TEXT};"
        )
        ui.button(primary_text, on_click=on_primary).props(
            "unelevated no-caps rounded"
        ).style(f"background-color: {primary_color}; color: white; min-width: 90px;")


# --- Dialogs publicos ---

async def show_add_expense(on_success: OnSuccess = None) -> None:
    """UC-02: Add expense (manual)."""
    cats = await get_categories()

    with ui.dialog() as dialog, _dialog_card():
        _dialog_title("Add expense")

        amount = ui.number("Amount", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full")
        desc = ui.input("Description (optional)").props("outlined dense").classes("w-full")
        d = _date_input("Date", default=date.today().isoformat())

        ui.label("Category").style(
            f"color: {theme.PRIMARY}; font-size: 13px; font-weight: 600; margin-top: 4px;"
        )
        cat_state = _category_chip_group(cats)

        async def submit() -> None:
            if not amount.value or amount.value <= 0:
                ui.notify("Amount must be greater than 0", type="warning")
                return
            if cat_state["selected_id"] is None:
                ui.notify("Pick a category", type="warning")
                return
            try:
                await api.create_expense(
                    float(amount.value),
                    (desc.value or "").strip() or "No description",
                    d.value or date.today().isoformat(),
                    cat_state["selected_id"],
                )
                dialog.close()
                ui.notify("Expense added", type="positive")
                if on_success:
                    await on_success()
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        _dialog_actions(dialog, "Save", submit)

    dialog.open()


async def show_create_budget(on_success: OnSuccess = None) -> None:
    """UC-03: Create monthly budget."""
    today = date.today()
    cats = await get_categories()

    with ui.dialog() as dialog, _dialog_card():
        _dialog_title("Create budget")

        ui.label("Category").style(
            f"color: {theme.PRIMARY}; font-size: 13px; font-weight: 600;"
        )
        cat_state = _category_chip_group(cats)

        amount = ui.number("Monthly limit", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full").style("margin-top: 8px;")

        async def submit() -> None:
            if not amount.value or amount.value <= 0:
                ui.notify("Limit must be greater than 0", type="warning")
                return
            if cat_state["selected_id"] is None:
                ui.notify("Pick a category", type="warning")
                return
            try:
                await api.create_budget(
                    cat_state["selected_id"], float(amount.value), today.month, today.year
                )
                dialog.close()
                ui.notify("Budget created", type="positive")
                if on_success:
                    await on_success()
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        _dialog_actions(dialog, "Save", submit)

    dialog.open()


async def show_create_goal(on_success: OnSuccess = None) -> None:
    """Crear meta de ahorro nueva."""
    with ui.dialog() as dialog, _dialog_card():
        _dialog_title("New savings goal")

        name = ui.input("What are you saving for?").props("outlined dense").classes("w-full")
        target = ui.number("Target amount", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full")
        d = _date_input("Deadline (optional)")

        async def submit() -> None:
            if not name.value or not name.value.strip():
                ui.notify("Name is required", type="warning")
                return
            if not target.value or target.value <= 0:
                ui.notify("Target must be greater than 0", type="warning")
                return
            try:
                await api.create_goal(
                    name.value.strip(), float(target.value), d.value if d.value else None
                )
                dialog.close()
                ui.notify("Goal created", type="positive")
                if on_success:
                    await on_success()
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        _dialog_actions(dialog, "Create", submit)

    dialog.open()


async def show_contribute_goal(goal_id: int, sign: int, on_success: OnSuccess = None) -> None:
    """Anadir o retirar dinero de una meta. Feedback clave del profesor."""
    title = "Add money" if sign > 0 else "Withdraw"
    quick_amounts = [5, 10, 25, 50] if sign > 0 else [5, 10, 25]

    with ui.dialog() as dialog, _dialog_card():
        _dialog_title(title)

        amount = ui.number("Amount", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full")

        with ui.row().classes("w-full gap-2 flex-wrap items-center").style("margin-top: 4px;"):
            ui.label("Quick:").style(f"color: {theme.GREY_TEXT}; font-size: 12px;")
            for q in quick_amounts:
                ui.button(
                    f"${q}",
                    on_click=lambda v=q: setattr(amount, "value", float(v)),
                ).props("outline dense no-caps rounded").style(
                    f"color: {theme.SECONDARY}; border-color: {theme.SECONDARY}; "
                    "min-width: 0; padding: 4px 12px;"
                )

        async def submit() -> None:
            if not amount.value or amount.value <= 0:
                ui.notify("Amount must be greater than 0", type="warning")
                return
            try:
                await api.contribute_goal(goal_id, sign * float(amount.value))
                dialog.close()
                verb = "Added" if sign > 0 else "Withdrew"
                ui.notify(f"{verb} {theme.fmt_money(amount.value)}", type="positive")
                if on_success:
                    await on_success()
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        _dialog_actions(dialog, "Confirm", submit)

    dialog.open()


AVATAR_OPTIONS = [
    "🦊", "🐱", "🐻", "🐼", "🐸", "🐰", "🦁", "🐨",
    "🌟", "🚀", "💎", "🎯", "🔥", "⚡", "🏆", "🎨",
]


async def show_avatar_picker(current: str | None, on_success: OnSuccess = None) -> None:
    """Selector de avatar emoji. Se persiste via PATCH /auth/me."""
    state = {"selected": current}

    with ui.dialog() as dialog, _dialog_card():
        _dialog_title("Choose your avatar")
        ui.label("Pick an emoji that represents you").style(
            f"color: {theme.GREY_TEXT}; font-size: 12px; margin-bottom: 8px;"
        )

        grid = ui.grid(columns=8).classes("w-full gap-2")

        def repaint() -> None:
            grid.clear()
            with grid:
                for emoji in AVATAR_OPTIONS:
                    is_sel = state["selected"] == emoji
                    bg = theme.SECONDARY if is_sel else theme.GREY_BG
                    label_color = theme.WHITE if is_sel else theme.PRIMARY
                    cell = ui.element("div").classes(
                        "cursor-pointer flex items-center justify-center"
                    ).style(
                        f"width: 100%; aspect-ratio: 1; border-radius: 12px; "
                        f"background: {bg}; font-size: 24px; "
                        f"box-shadow: {('0 2px 8px ' + theme.SECONDARY + '66') if is_sel else 'none'}; "
                        f"color: {label_color}; transition: all 0.15s ease;"
                    )
                    with cell:
                        ui.label(emoji).style("font-size: 24px; line-height: 1;")
                    cell.on("click", lambda e=emoji: _select(e))

        def _select(emoji: str) -> None:
            state["selected"] = emoji
            repaint()

        repaint()

        async def submit() -> None:
            if not state["selected"]:
                ui.notify("Pick an emoji first", type="warning")
                return
            try:
                await api.update_avatar(state["selected"])
                dialog.close()
                ui.notify("Avatar updated", type="positive")
                if on_success:
                    await on_success()
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        _dialog_actions(dialog, "Save", submit)

    dialog.open()


def show_confirm(message: str, on_confirm: Callable[[], Awaitable[None]],
                 confirm_text: str = "Delete", danger: bool = True) -> None:
    """Confirmacion generica con accion async."""
    with ui.dialog() as dialog, ui.card().style(
        "border-radius: 14px; padding: 20px; min-width: 280px; max-width: 92vw;"
    ):
        ui.label(message).style(
            f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 600;"
        )
        with ui.row().classes("w-full justify-end gap-2").style("margin-top: 8px;"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps").style(
                f"color: {theme.GREY_TEXT};"
            )

            async def go() -> None:
                try:
                    await on_confirm()
                    dialog.close()
                except api.ApiException as e:
                    ui.notify(f"Error: {e.message}", type="negative")

            ui.button(confirm_text, on_click=go).props(
                "unelevated no-caps rounded"
            ).style(
                f"background-color: {theme.ERROR if danger else theme.SECONDARY}; "
                "color: white; min-width: 90px;"
            )

    dialog.open()

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
        f"width: 380px; max-width: 94vw; border-radius: 24px; padding: 24px; "
        f"background: {theme.WHITE}; box-shadow: 0 24px 64px rgba(0,0,0,0.18);"
    )


def _dialog_title(text: str) -> None:
    ui.label(text).style(
        f"color: {theme.PRIMARY}; font-size: 19px; font-weight: 800; "
        "letter-spacing: -0.3px; margin-bottom: 6px;"
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
        _dialog_title("Add Expense")

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
                ui.notify("Please enter a valid amount", type="warning")
                return
            if cat_state["selected_id"] is None:
                ui.notify("Please select a category", type="warning")
                return
            try:
                await api.create_expense(
                    float(amount.value),
                    (desc.value or "").strip() or "Expense",
                    d.value or date.today().isoformat(),
                    cat_state["selected_id"],
                )
                dialog.close()
                ui.notify("Expense recorded", type="positive")
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
        _dialog_title("Set Budget")

        ui.label("Category").style(
            f"color: {theme.PRIMARY}; font-size: 13px; font-weight: 600;"
        )
        cat_state = _category_chip_group(cats)

        amount = ui.number("Monthly limit", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full").style("margin-top: 8px;")

        async def submit() -> None:
            if not amount.value or amount.value <= 0:
                ui.notify("Please enter a valid limit", type="warning")
                return
            if cat_state["selected_id"] is None:
                ui.notify("Please select a category", type="warning")
                return
            try:
                await api.create_budget(
                    cat_state["selected_id"], float(amount.value), today.month, today.year
                )
                dialog.close()
                ui.notify("Budget saved", type="positive")
                if on_success:
                    await on_success()
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        _dialog_actions(dialog, "Save", submit)

    dialog.open()


async def show_create_goal(on_success: OnSuccess = None) -> None:
    """Crear meta de ahorro nueva."""
    with ui.dialog() as dialog, _dialog_card():
        _dialog_title("New Goal")

        name = ui.input("Goal name").props("outlined dense").classes("w-full")
        target = ui.number("Target amount", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full")
        d = _date_input("Deadline (optional)")

        async def submit() -> None:
            if not name.value or not name.value.strip():
                ui.notify("Goal name is required", type="warning")
                return
            if not target.value or target.value <= 0:
                ui.notify("Please enter a valid target amount", type="warning")
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
                ui.notify("Please enter a valid amount", type="warning")
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


async def show_avatar_picker(current: str | None, on_success: OnSuccess = None) -> None:
    """Subir foto de perfil. Se redimensiona client-side a 256x256 (canvas) y
    se persiste como data URL JPEG en /auth/me. Tambien permite eliminarla.
    """
    import base64

    state = {"data_url": current}

    with ui.dialog() as dialog, _dialog_card():
        _dialog_title("Update Photo")
        ui.label("Upload a profile photo. Images are automatically optimised.").style(
            f"color: {theme.GREY_TEXT}; font-size: 12px; margin-bottom: 8px;"
        )

        # Preview circular
        preview_container = ui.element("div").classes(
            "self-center flex items-center justify-center"
        ).style(
            f"width: 120px; height: 120px; border-radius: 50%; overflow: hidden; "
            f"background: {theme.GREY_BG}; margin: 8px auto;"
        )

        def render_preview() -> None:
            preview_container.clear()
            with preview_container:
                if state["data_url"] and state["data_url"].startswith("data:"):
                    ui.image(state["data_url"]).style(
                        "width: 100%; height: 100%; object-fit: cover;"
                    )
                else:
                    ui.icon("person").style(
                        f"color: {theme.GREY_SOFT}; font-size: 64px;"
                    )

        render_preview()

        async def handle_upload(e) -> None:
            try:
                content = e.content.read()
                mime = e.type or "image/jpeg"
                data_url = f"data:{mime};base64,{base64.b64encode(content).decode()}"
            except Exception:
                ui.notify("Could not read the photo — please try another file", type="warning")
                return
            if len(data_url) > 480_000:
                ui.notify("Image too large — please choose a smaller photo (max ~350KB)", type="warning")
                return
            state["data_url"] = data_url
            render_preview()
            ui.notify("Photo ready — tap Save to confirm", type="info")

        upload = ui.upload(
            on_upload=handle_upload,
            max_files=1,
            auto_upload=True,
        ).props('accept="image/*" flat color=primary label="Choose photo"').classes("w-full")
        upload.style("border: 2px dashed " + theme.GREY_SOFT + "; border-radius: 12px; padding: 8px;")

        if current:
            ui.button("Remove photo", on_click=lambda: _clear()).props(
                "flat no-caps dense"
            ).style(f"color: {theme.ERROR};")

        def _clear() -> None:
            state["data_url"] = ""
            render_preview()

        async def submit() -> None:
            try:
                # "" para borrar; data URL para guardar
                await api.update_avatar(state["data_url"] or "")
                dialog.close()
                ui.notify("Profile updated", type="positive")
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

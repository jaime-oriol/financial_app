"""Budget tracker. UC-02 (add expense), UC-03 (create budget), UC-04 (view history).
Donut chart de spending, barras de presupuesto con progress real, lista de gastos
con accion de eliminar (CRUD completo, todo transaccional).
"""

from datetime import date

from nicegui import ui

import api
import theme
from layout import (
    app_shell,
    card,
    empty_state,
    outlined_button,
    primary_button,
    require_auth,
    section,
)


@ui.page("/budget")
async def budget_page():
    if not require_auth():
        return

    # Estado mutable de la pagina (para refrescar tras crear/eliminar)
    refs: dict = {}

    with app_shell(active="/budget"):
        with section(top=22):
            ui.label("Budget").style(
                f"color: {theme.PRIMARY}; font-size: 24px; font-weight: 800;"
            )
            ui.label("Track spending and set monthly limits").style(
                f"color: {theme.GREY_TEXT}; font-size: 13px;"
            )

        # Donut chart card
        with section():
            with card():
                ui.label("Spending this month").style(
                    f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 700;"
                )
                refs["chart"] = ui.column().classes("w-full items-center gap-2")

        # Category budgets
        with section("Category budgets"):
            refs["budgets"] = ui.column().classes("w-full gap-2")

        # Recent expenses (CRUD completo: poder eliminar)
        with section("Recent expenses"):
            refs["expenses"] = ui.column().classes("w-full gap-2")

        # Action buttons
        with section():
            primary_button(
                "Add expense", lambda: _add_expense_dialog(refs), icon="add"
            )
        with section(top=8):
            outlined_button(
                "New budget", lambda: _create_budget_dialog(refs), icon="pie_chart_outline"
            )
            ui.element("div").style("height: 16px;")

        await _reload(refs)


async def _reload(refs: dict) -> None:
    """Recargar datos del backend y re-renderizar las secciones."""
    try:
        dashboard = await api.get_dashboard()
        budgets = dashboard.get("budgets", [])
        spending = dashboard.get("spending_by_category", [])
        expenses = await api.get_expenses()
    except api.ApiException as e:
        if e.status in (401, 403):
            ui.navigate.to("/login")
            return
        ui.notify(f"Error: {e.message}", type="negative")
        return

    _render_chart(refs["chart"], spending)
    _render_budgets(refs["budgets"], budgets, refs)
    _render_expenses(refs["expenses"], expenses, refs)


def _render_chart(container: ui.column, spending: list[dict]) -> None:
    container.clear()
    with container:
        if not spending:
            empty_state("donut_large", "No spending yet this month")
            return
        ui.echart(
            {
                "tooltip": {"trigger": "item", "formatter": "{b}: ${c} ({d}%)"},
                "legend": {"show": False},
                "series": [
                    {
                        "name": "Spending",
                        "type": "pie",
                        "radius": ["55%", "78%"],
                        "center": ["50%", "50%"],
                        "avoidLabelOverlap": True,
                        "itemStyle": {"borderRadius": 6, "borderColor": "#fff", "borderWidth": 2},
                        "label": {"show": False},
                        "emphasis": {"label": {"show": True, "fontWeight": "bold"}},
                        "data": [
                            {
                                "value": float(s["total"]),
                                "name": s["category_name"],
                                "itemStyle": {"color": theme.category_color(s["category_id"])},
                            }
                            for s in spending
                        ],
                    }
                ],
            }
        ).style("height: 220px; width: 100%;")
        # Leyenda manual debajo
        with ui.row().classes("w-full justify-center gap-3 flex-wrap"):
            for s in spending:
                with ui.row().classes("items-center gap-1"):
                    ui.element("div").style(
                        f"width: 10px; height: 10px; border-radius: 50%; "
                        f"background-color: {theme.category_color(s['category_id'])};"
                    )
                    ui.label(s["category_name"]).style(
                        f"color: {theme.PRIMARY}; font-size: 12px;"
                    )


def _render_budgets(container: ui.column, budgets: list[dict], refs: dict) -> None:
    container.clear()
    with container:
        if not budgets:
            with card():
                empty_state("savings", "No budgets yet. Create one to start tracking!")
            return
        for b in budgets:
            _budget_row(b, refs)


def _budget_row(b: dict, refs: dict) -> None:
    color = theme.category_color(b["category_id"])
    progress = b["progress"]
    bar_color = theme.ERROR if progress > 90 else color

    with ui.row().classes("w-full no-wrap items-stretch gap-0").style(
        f"background: {theme.WHITE}; border-radius: 14px; "
        "box-shadow: 0 2px 8px rgba(0,0,0,0.04); overflow: hidden;"
    ):
        # Barra de color a la izquierda
        ui.element("div").style(f"width: 4px; background-color: {color};")
        with ui.column().classes("flex-1 gap-2").style("padding: 14px;"):
            with ui.row().classes("w-full items-center gap-2 no-wrap"):
                ui.icon(theme.category_icon(b["category_id"])).style(
                    f"color: {color}; font-size: 20px;"
                )
                ui.label(b.get("category_name") or "Category").classes("flex-1").style(
                    f"color: {theme.PRIMARY}; font-size: 14px; font-weight: 600;"
                )
                ui.label(theme.fmt_money(b["spent"], 0)).style(
                    f"color: {bar_color}; font-size: 14px; font-weight: 700;"
                )
                ui.label(f" / {theme.fmt_money(b['limit_amount'], 0)}").style(
                    f"color: {theme.GREY_TEXT}; font-size: 12px;"
                )
                ui.button(icon="delete_outline").props("flat dense round").style(
                    f"color: {theme.GREY_SOFT};"
                ).on(
                    "click", lambda bid=b["budget_id"]: _confirm_delete_budget(bid, refs)
                )
            ui.linear_progress(
                value=min(progress / 100, 1.0), show_value=False, size="6px"
            ).props(f"rounded color={'red' if progress > 90 else 'primary'}").style(
                f"--q-primary: {bar_color};"
            )


def _render_expenses(container: ui.column, expenses: list[dict], refs: dict) -> None:
    container.clear()
    with container:
        if not expenses:
            with card():
                empty_state("receipt_long", "No expenses yet")
            return
        with card(padding=4):
            for i, e in enumerate(expenses[:20]):
                if i > 0:
                    ui.separator().style(f"background-color: {theme.GREY_BG};")
                _expense_row(e, refs)


def _expense_row(expense: dict, refs: dict) -> None:
    color = theme.category_color(expense["category_id"])
    with ui.row().classes("w-full items-center no-wrap gap-3").style("padding: 10px;"):
        with ui.element("div").style(
            f"background: {color}26; width: 38px; height: 38px; "
            "border-radius: 10px; display: flex; align-items: center; "
            "justify-content: center; flex-shrink: 0;"
        ):
            ui.icon(theme.category_icon(expense["category_id"])).style(
                f"color: {color}; font-size: 18px;"
            )
        with ui.column().classes("flex-1 gap-0").style("min-width: 0;"):
            ui.label(expense.get("category_name") or "Expense").style(
                f"color: {theme.PRIMARY}; font-size: 13px; font-weight: 600;"
            )
            ui.label(f"{expense['description']} · {expense['expense_date']}").style(
                f"color: {theme.GREY_TEXT}; font-size: 11px; "
                "overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
            )
        ui.label(f"-{theme.fmt_money(expense['amount'])}").style(
            f"color: {theme.ERROR}; font-size: 13px; font-weight: 700;"
        )
        ui.button(icon="delete_outline").props("flat dense round size=sm").style(
            f"color: {theme.GREY_SOFT};"
        ).on("click", lambda eid=expense["expense_id"]: _confirm_delete_expense(eid, refs))


# --- Dialogos ---

def _add_expense_dialog(refs: dict) -> None:
    with ui.dialog() as dialog, ui.card().style(
        f"width: 360px; border-radius: 16px; padding: 22px; background: {theme.WHITE};"
    ):
        ui.label("Add expense").style(
            f"color: {theme.PRIMARY}; font-size: 18px; font-weight: 700;"
        )
        amount = ui.number("Amount", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full")
        desc = ui.input("Description (optional)").props("outlined dense").classes("w-full")
        d = ui.input("Date", value=date.today().isoformat()).props(
            "outlined dense readonly"
        ).classes("w-full")
        with d.add_slot("append"):
            ui.icon("event").classes("cursor-pointer").on(
                "click", lambda: date_dialog.open()
            )
        with ui.dialog() as date_dialog, ui.card():
            ui.date(
                value=date.today().isoformat(),
                on_change=lambda e: setattr(d, "value", e.value),
            ).props("mask=YYYY-MM-DD")
            ui.button("OK", on_click=date_dialog.close).props("flat")

        ui.label("Category").style(
            f"color: {theme.PRIMARY}; font-size: 13px; font-weight: 600; margin-top: 6px;"
        )
        cats_row = ui.row().classes("w-full gap-1 flex-wrap")
        selected = {"id": None}

        async def submit():
            if not amount.value or amount.value <= 0:
                ui.notify("Amount must be greater than 0", type="warning")
                return
            if selected["id"] is None:
                ui.notify("Pick a category", type="warning")
                return
            try:
                await api.create_expense(
                    float(amount.value),
                    desc.value.strip() or "No description",
                    d.value,
                    selected["id"],
                )
                dialog.close()
                ui.notify("Expense added", type="positive")
                await _reload(refs)
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        with ui.row().classes("w-full justify-end gap-2").style("margin-top: 12px;"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps").style(
                f"color: {theme.GREY_TEXT};"
            )
            ui.button("Save", on_click=submit).props("unelevated no-caps").style(
                f"background-color: {theme.SECONDARY}; color: white;"
            )

    async def load_cats():
        try:
            cats = await api.get_categories()
        except api.ApiException:
            return
        with cats_row:
            for c in cats:
                _make_chip(c, cats_row, selected)

    dialog.open()
    ui.timer(0.05, load_cats, once=True)


def _create_budget_dialog(refs: dict) -> None:
    today = date.today()

    with ui.dialog() as dialog, ui.card().style(
        f"width: 360px; border-radius: 16px; padding: 22px; background: {theme.WHITE};"
    ):
        ui.label("Create budget").style(
            f"color: {theme.PRIMARY}; font-size: 18px; font-weight: 700;"
        )
        ui.label("Category").style(
            f"color: {theme.PRIMARY}; font-size: 13px; font-weight: 600;"
        )
        cats_row = ui.row().classes("w-full gap-1 flex-wrap")
        selected = {"id": None}

        amount = ui.number("Monthly limit", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full").style("margin-top: 8px;")

        async def submit():
            if not amount.value or amount.value <= 0:
                ui.notify("Limit must be greater than 0", type="warning")
                return
            if selected["id"] is None:
                ui.notify("Pick a category", type="warning")
                return
            try:
                await api.create_budget(
                    selected["id"], float(amount.value), today.month, today.year
                )
                dialog.close()
                ui.notify("Budget created", type="positive")
                await _reload(refs)
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        with ui.row().classes("w-full justify-end gap-2").style("margin-top: 12px;"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps").style(
                f"color: {theme.GREY_TEXT};"
            )
            ui.button("Save", on_click=submit).props("unelevated no-caps").style(
                f"background-color: {theme.SECONDARY}; color: white;"
            )

    async def load_cats():
        try:
            cats = await api.get_categories()
        except api.ApiException:
            return
        with cats_row:
            for c in cats:
                _make_chip(c, cats_row, selected)

    dialog.open()
    ui.timer(0.05, load_cats, once=True)


def _make_chip(cat: dict, container: ui.row, selected: dict) -> None:
    color = theme.category_color(cat["category_id"])

    chip = ui.button(
        cat["name"],
        icon=theme.category_icon(cat["category_id"]),
    ).props("dense no-caps unelevated rounded")

    def update_styles():
        if selected["id"] == cat["category_id"]:
            chip.style(
                f"background-color: {color}33; color: {theme.PRIMARY}; "
                f"border: 1.5px solid {color}; font-weight: 600;"
            )
        else:
            chip.style(
                f"background-color: {theme.GREY_BG}; color: {theme.GREY_TEXT}; "
                "border: 1.5px solid transparent;"
            )

    def select():
        selected["id"] = cat["category_id"]
        for child in container.default_slot.children:
            # No tenemos referencia directa a cada chip; usamos JS event-less re-render
            pass
        update_styles()
        # Hack: forzar repaint de hermanos quitando el seleccionado de los demas
        for c in container.default_slot.children:
            if isinstance(c, ui.button) and c is not chip:
                c.style(
                    f"background-color: {theme.GREY_BG}; color: {theme.GREY_TEXT}; "
                    "border: 1.5px solid transparent;"
                )

    chip.on("click", select)
    update_styles()


# --- Confirmaciones de borrado ---

def _confirm_delete_expense(expense_id: int, refs: dict) -> None:
    with ui.dialog() as dialog, ui.card().style(
        "border-radius: 14px; padding: 18px; min-width: 280px;"
    ):
        ui.label("Delete this expense?").style(
            f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 600;"
        )
        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps")

            async def go():
                try:
                    await api.delete_expense(expense_id)
                    dialog.close()
                    ui.notify("Expense deleted", type="positive")
                    await _reload(refs)
                except api.ApiException as e:
                    ui.notify(f"Error: {e.message}", type="negative")

            ui.button("Delete", on_click=go).props("unelevated no-caps").style(
                f"background-color: {theme.ERROR}; color: white;"
            )
    dialog.open()


def _confirm_delete_budget(budget_id: int, refs: dict) -> None:
    with ui.dialog() as dialog, ui.card().style(
        "border-radius: 14px; padding: 18px; min-width: 280px;"
    ):
        ui.label("Delete this budget?").style(
            f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 600;"
        )
        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps")

            async def go():
                try:
                    await api.delete_budget(budget_id)
                    dialog.close()
                    ui.notify("Budget deleted", type="positive")
                    await _reload(refs)
                except api.ApiException as e:
                    ui.notify(f"Error: {e.message}", type="negative")

            ui.button("Delete", on_click=go).props("unelevated no-caps").style(
                f"background-color: {theme.ERROR}; color: white;"
            )
    dialog.open()

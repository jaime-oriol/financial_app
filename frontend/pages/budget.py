"""Budget tracker. UC-02 (add expense), UC-03 (create budget), UC-04 (view history).
Donut chart con total en el centro, barras de progreso, lista de gastos con
delete inline. Todos los dialogs vienen de dialogs.py (DRY).
"""

from nicegui import ui

import api
import dialogs
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

    refs: dict = {}

    async def reload() -> None:
        try:
            dashboard = await api.get_dashboard()
            expenses = await api.get_expenses()
        except api.ApiException as e:
            if e.status in (401, 403):
                ui.navigate.to("/login")
                return
            ui.notify(f"Error: {e.message}", type="negative")
            return
        _render_chart(refs["chart"], dashboard.get("spending_by_category", []))
        _render_budgets(refs["budgets"], dashboard.get("budgets", []), reload)
        _render_expenses(refs["expenses"], expenses, reload)

    with app_shell(active="/budget"):
        with section(top=22):
            ui.label("Budget").style(
                f"color: {theme.PRIMARY}; font-size: 24px; font-weight: 800;"
            )
            ui.label("Track spending and set monthly limits").style(
                f"color: {theme.GREY_TEXT}; font-size: 13px;"
            )

        with section():
            with card():
                ui.label("Spending this month").style(
                    f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 700;"
                )
                refs["chart"] = ui.column().classes("w-full items-center gap-2")

        with section("Category budgets"):
            refs["budgets"] = ui.column().classes("w-full gap-2")

        with section("Recent expenses"):
            refs["expenses"] = ui.column().classes("w-full gap-2")

        with section():
            primary_button(
                "Add expense",
                lambda: dialogs.show_add_expense(on_success=reload),
                icon="add",
            )
        with section(top=8):
            outlined_button(
                "New budget",
                lambda: dialogs.show_create_budget(on_success=reload),
                icon="pie_chart_outline",
            )
            ui.element("div").style("height: 16px;")

    await reload()


def _render_chart(container: ui.column, spending: list[dict]) -> None:
    container.clear()
    with container:
        if not spending:
            empty_state("donut_large", "No spending yet this month")
            return
        total = sum(float(s["total"]) for s in spending)
        ui.echart(
            {
                "tooltip": {
                    "trigger": "item",
                    "formatter": "{b}: ${c} ({d}%)",
                    "backgroundColor": theme.PRIMARY,
                    "borderColor": theme.PRIMARY,
                    "textStyle": {"color": "#fff", "fontSize": 12},
                },
                "graphic": [
                    {
                        "type": "text",
                        "left": "center",
                        "top": "42%",
                        "style": {
                            "text": f"${total:,.0f}",
                            "fill": theme.PRIMARY,
                            "fontSize": 22,
                            "fontWeight": 800,
                        },
                    },
                    {
                        "type": "text",
                        "left": "center",
                        "top": "55%",
                        "style": {
                            "text": "this month",
                            "fill": theme.GREY_TEXT,
                            "fontSize": 11,
                            "fontWeight": 500,
                        },
                    },
                ],
                "series": [
                    {
                        "name": "Spending",
                        "type": "pie",
                        "radius": ["55%", "78%"],
                        "center": ["50%", "50%"],
                        "avoidLabelOverlap": True,
                        "itemStyle": {
                            "borderRadius": 6,
                            "borderColor": "#fff",
                            "borderWidth": 2,
                        },
                        "label": {"show": False},
                        "labelLine": {"show": False},
                        "data": [
                            {
                                "value": float(s["total"]),
                                "name": s["category_name"],
                                "itemStyle": {
                                    "color": theme.category_color(s["category_id"])
                                },
                            }
                            for s in spending
                        ],
                    }
                ],
            }
        ).style("height: 220px; width: 100%;")
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


def _render_budgets(container: ui.column, budgets: list[dict], reload) -> None:
    container.clear()
    with container:
        if not budgets:
            with card():
                empty_state("savings", "No budgets yet. Create one to start tracking!")
            return
        for b in budgets:
            _budget_row(b, reload)


def _budget_row(b: dict, reload) -> None:
    color = theme.category_color(b["category_id"])
    progress = b["progress"]
    bar_color = theme.ERROR if progress > 90 else color

    async def do_delete() -> None:
        await api.delete_budget(b["budget_id"])
        ui.notify("Budget deleted", type="positive")
        await reload()

    with ui.row().classes("w-full no-wrap items-stretch gap-0").style(
        f"background: {theme.WHITE}; border-radius: 14px; "
        "box-shadow: 0 2px 8px rgba(0,0,0,0.04); overflow: hidden;"
    ):
        ui.element("div").style(f"width: 4px; background-color: {color};")
        with ui.column().classes("flex-1 gap-2").style("padding: 14px;"):
            with ui.row().classes("w-full items-center gap-2 no-wrap"):
                ui.icon(theme.category_icon(b["category_id"])).style(
                    f"color: {color}; font-size: 20px;"
                )
                ui.label(b.get("category_name") or "Category").classes("flex-1").style(
                    f"color: {theme.PRIMARY}; font-size: 14px; font-weight: 600;"
                )
                ui.label(theme.fmt_money(b["spent"], 0)).classes("fapp-money").style(
                    f"color: {bar_color}; font-size: 14px; font-weight: 700;"
                )
                ui.label(f" / {theme.fmt_money(b['limit_amount'], 0)}").classes(
                    "fapp-money"
                ).style(f"color: {theme.GREY_TEXT}; font-size: 12px;")
                ui.button(icon="delete_outline").props("flat dense round").style(
                    f"color: {theme.GREY_SOFT};"
                ).on(
                    "click",
                    lambda: dialogs.show_confirm("Delete this budget?", do_delete),
                )
            ui.linear_progress(
                value=min(progress / 100, 1.0), show_value=False, size="6px"
            ).props("rounded").style(f"--q-primary: {bar_color};")


def _render_expenses(container: ui.column, expenses: list[dict], reload) -> None:
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
                _expense_row(e, reload)


def _expense_row(expense: dict, reload) -> None:
    color = theme.category_color(expense["category_id"])

    async def do_delete() -> None:
        await api.delete_expense(expense["expense_id"])
        ui.notify("Expense deleted", type="positive")
        await reload()

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
        ui.label(f"-{theme.fmt_money(expense['amount'])}").classes("fapp-money").style(
            f"color: {theme.ERROR}; font-size: 13px; font-weight: 700;"
        )
        ui.button(icon="delete_outline").props("flat dense round size=sm").style(
            f"color: {theme.GREY_SOFT};"
        ).on(
            "click",
            lambda: dialogs.show_confirm("Delete this expense?", do_delete),
        )

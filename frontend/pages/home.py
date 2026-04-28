"""Home / Dashboard. UC-05: View dashboard / simple analytics.
Todo transaccional: greeting (de /auth/me), spending real, streak real (calculada
desde expenses), budget %, recent transactions. Sin mocks.

Optimizaciones:
- /auth/me y /dashboard se piden en paralelo con asyncio.gather (latencia ↓)
- FAB abre el dialog "Add expense" directamente (1 click menos vs ir a /budget)
- Reload tras crear gasto sin recargar la pagina entera
"""

import asyncio
from datetime import datetime

from nicegui import ui

import api
import dialogs
import theme
from layout import app_shell, card, empty_state, require_auth, section


def _greeting() -> str:
    h = datetime.now().hour
    if h < 12:
        return "Good morning"
    if h < 19:
        return "Good afternoon"
    return "Good evening"


@ui.page("/")
async def home_page():
    if not require_auth():
        return

    refs: dict = {}

    async def reload() -> None:
        try:
            me, dashboard = await asyncio.gather(api.get_me(), api.get_dashboard())
        except api.ApiException as e:
            if e.status in (401, 403):
                ui.navigate.to("/login")
                return
            ui.notify(f"Error: {e.message}", type="negative")
            return

        refs["greeting"].text = f"{_greeting()}, {me['name']}!"

        spending = dashboard.get("spending_by_category", [])
        total = sum(float(s["total"]) for s in spending)
        refs["total"].text = theme.fmt_money(total)
        _render_breakdown(refs["stripe"], refs["legend"], spending, total)

        streak = dashboard.get("streak", 0)
        refs["streak"].text = f"{streak} day{'s' if streak != 1 else ''}"

        budgets = dashboard.get("budgets", [])
        if budgets:
            avg = sum(b["progress"] for b in budgets) / len(budgets)
            refs["budget_pct"].text = f"{avg:.0f}%"
            refs["budget_pct"].style(
                f"color: {theme.ERROR if avg > 90 else theme.SECONDARY};"
            )
        else:
            refs["budget_pct"].text = "—"
            refs["budget_pct"].style(f"color: {theme.GREY_SOFT};")

        _render_recent(refs["recent"], dashboard.get("recent_transactions", []))

    with app_shell(active="/"):
        # Header con saludo + total del mes (gradiente sutil)
        with ui.column().classes("w-full gap-1").style(
            "background: linear-gradient(135deg, #16213E 0%, #1F3260 100%); "
            "padding: 36px 22px 24px 22px; "
            "border-bottom-left-radius: 24px; border-bottom-right-radius: 24px;"
        ):
            refs["greeting"] = ui.label(_greeting()).style(
                f"color: {theme.GREY_SOFT}; font-size: 14px;"
            )
            ui.label("Total spending this month").style(
                "color: rgba(255,255,255,0.7); font-size: 11px; "
                "font-weight: 600; letter-spacing: 1px; text-transform: uppercase;"
            )
            refs["total"] = ui.label("$0.00").classes("fapp-money").style(
                f"color: {theme.WHITE}; font-size: 36px; font-weight: 800;"
            )
            refs["stripe"] = ui.row().classes("w-full gap-0").style(
                "height: 8px; border-radius: 4px; overflow: hidden; "
                "margin-top: 8px; background: rgba(255,255,255,0.15);"
            )
            refs["legend"] = ui.row().classes("w-full gap-3 flex-wrap").style(
                "margin-top: 6px; min-height: 18px;"
            )

        # Stats: streak | budget %
        with ui.row().classes("w-full gap-2 no-wrap").style("padding: 16px;"):
            with ui.column().classes("flex-1 fapp-card gap-1"):
                ui.label("Streak").classes("fapp-section-label")
                with ui.row().classes("items-center gap-1"):
                    refs["streak"] = ui.label("0 days").classes("fapp-stat-num")
                    ui.icon("local_fire_department").style(
                        f"color: {theme.WARNING}; font-size: 24px;"
                    )
            with ui.column().classes("flex-1 fapp-card gap-1"):
                ui.label("Budget used").classes("fapp-section-label")
                refs["budget_pct"] = ui.label("0%").classes("fapp-stat-num").style(
                    f"color: {theme.SECONDARY};"
                )

        # Recent transactions
        with section("Recent transactions"):
            refs["recent"] = ui.column().classes("w-full gap-2")

        # FAB: abre el dialog directamente (no navega)
        with ui.page_sticky(position="bottom-right", x_offset=18, y_offset=82):
            ui.button(
                icon="add",
                on_click=lambda: dialogs.show_add_expense(on_success=reload),
            ).props("fab color=primary").style(
                f"background-color: {theme.SECONDARY}; color: white;"
            ).tooltip("Add expense")

    await reload()


def _render_breakdown(stripe: ui.row, legend: ui.row, spending: list[dict], total: float) -> None:
    stripe.clear()
    legend.clear()
    if not spending or total <= 0:
        return
    with stripe:
        for s in spending:
            pct = float(s["total"]) / total * 100
            ui.element("div").style(
                f"flex: {max(pct, 1)}; background-color: "
                f"{theme.category_color(s['category_id'])}; height: 100%;"
            )
    with legend:
        for s in spending:
            with ui.row().classes("items-center gap-1"):
                ui.element("div").style(
                    f"width: 8px; height: 8px; border-radius: 50%; "
                    f"background-color: {theme.category_color(s['category_id'])};"
                )
                ui.label(
                    f"{s['category_name']} {theme.fmt_money(s['total'], 0)}"
                ).style("color: rgba(255,255,255,0.85); font-size: 11px;")


def _render_recent(container: ui.column, expenses: list[dict]) -> None:
    container.clear()
    with container:
        if not expenses:
            with card():
                empty_state(
                    "receipt_long",
                    "No expenses yet. Tap the + button to add your first one.",
                )
            return
        with card(padding=8):
            for i, e in enumerate(expenses):
                if i > 0:
                    ui.separator().style(f"background-color: {theme.GREY_BG};")
                _transaction_row(e)


def _transaction_row(expense: dict) -> None:
    color = theme.category_color(expense["category_id"])
    with ui.row().classes("w-full items-center no-wrap gap-3").style("padding: 10px;"):
        with ui.element("div").style(
            f"background: {color}26; width: 40px; height: 40px; "
            "border-radius: 10px; display: flex; align-items: center; "
            "justify-content: center; flex-shrink: 0;"
        ):
            ui.icon(theme.category_icon(expense["category_id"])).style(
                f"color: {color}; font-size: 20px;"
            )
        with ui.column().classes("flex-1 gap-0").style("min-width: 0;"):
            ui.label(expense.get("category_name") or "Expense").style(
                f"color: {theme.PRIMARY}; font-size: 14px; font-weight: 600;"
            )
            ui.label(expense["description"]).style(
                f"color: {theme.GREY_TEXT}; font-size: 12px; "
                "overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
            )
        ui.label(f"-{theme.fmt_money(expense['amount'])}").classes("fapp-money").style(
            f"color: {theme.ERROR}; font-size: 14px; font-weight: 700;"
        )

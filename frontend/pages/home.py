"""Home / Dashboard. UC-05: View dashboard / simple analytics.
Todo transaccional: greeting (de /auth/me), spending by category, streak (real,
calculada desde expenses), budget %, recent transactions. Sin mocks.
"""

from datetime import datetime

from nicegui import ui

import api
import theme
from layout import app_shell, card, empty_state, primary_button, require_auth, section


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

    with app_shell(active="/"):
        # Header oscuro con saludo + total del mes
        header_container = ui.column().classes("w-full gap-1").style(
            f"background-color: {theme.PRIMARY}; padding: 36px 22px 24px 22px; "
            "border-bottom-left-radius: 24px; border-bottom-right-radius: 24px;"
        )
        with header_container:
            greeting_label = ui.label(f"{_greeting()}").style(
                f"color: {theme.GREY_SOFT}; font-size: 14px;"
            )
            ui.label("Total spending this month").style(
                "color: rgba(255,255,255,0.7); font-size: 11px; "
                "font-weight: 600; letter-spacing: 1px; text-transform: uppercase;"
            )
            total_label = ui.label("$0.00").style(
                f"color: {theme.WHITE}; font-size: 36px; font-weight: 800;"
            )
            stripe = ui.row().classes("w-full gap-0").style(
                "height: 8px; border-radius: 4px; overflow: hidden; "
                "margin-top: 8px; background: rgba(255,255,255,0.15);"
            )
            legend = ui.row().classes("w-full gap-3 flex-wrap").style("margin-top: 6px;")

        # Stats row: streak | budget %
        stats_row = ui.row().classes("w-full gap-2 no-wrap").style("padding: 16px;")
        with stats_row:
            with ui.column().classes("flex-1 fapp-card gap-1"):
                ui.label("Streak").classes("fapp-section-label")
                streak_row = ui.row().classes("items-center gap-1")
                with streak_row:
                    streak_label = ui.label("0 days").classes("fapp-stat-num")
                    ui.icon("local_fire_department").style(
                        f"color: {theme.WARNING}; font-size: 24px;"
                    )
            with ui.column().classes("flex-1 fapp-card gap-1"):
                ui.label("Budget used").classes("fapp-section-label")
                budget_pct_label = ui.label("0%").classes("fapp-stat-num").style(
                    f"color: {theme.SECONDARY};"
                )

        # Recent transactions
        with section("Recent transactions"):
            recent_container = ui.column().classes("w-full gap-2")

        # FAB: add expense — siempre visible
        with ui.page_sticky(position="bottom-right", x_offset=18, y_offset=82):
            ui.button(icon="add", on_click=lambda: ui.navigate.to("/budget")).props(
                "fab color=primary"
            ).style(f"background-color: {theme.SECONDARY}; color: white;")

        # --- Cargar datos del backend ---
        try:
            me = await api.get_me()
            greeting_label.text = f"{_greeting()}, {me['name']}!"
        except api.ApiException:
            pass

        try:
            data = await api.get_dashboard()
        except api.ApiException as e:
            if e.status in (401, 403):
                ui.navigate.to("/login")
                return
            ui.notify(f"Error: {e.message}", type="negative")
            return

        # Total + barra segmentada + leyenda
        spending = data.get("spending_by_category", [])
        total = sum(float(s["total"]) for s in spending)
        total_label.text = theme.fmt_money(total)

        stripe.clear()
        legend.clear()
        if spending:
            with stripe:
                for s in spending:
                    pct = (float(s["total"]) / total * 100) if total else 0
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

        # Streak
        streak = data.get("streak", 0)
        streak_label.text = f"{streak} day{'s' if streak != 1 else ''}"

        # Budget %
        budgets = data.get("budgets", [])
        if budgets:
            avg = sum(b["progress"] for b in budgets) / len(budgets)
            budget_pct_label.text = f"{avg:.0f}%"
            if avg > 90:
                budget_pct_label.style(f"color: {theme.ERROR};")

        # Recent transactions
        recent = data.get("recent_transactions", [])
        recent_container.clear()
        with recent_container:
            if not recent:
                with card():
                    empty_state(
                        "receipt_long",
                        "No expenses yet. Add one from the Budget tab to get started!",
                    )
            else:
                with card(padding=8):
                    for i, e in enumerate(recent):
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
        ui.label(f"-{theme.fmt_money(expense['amount'])}").style(
            f"color: {theme.ERROR}; font-size: 14px; font-weight: 700;"
        )

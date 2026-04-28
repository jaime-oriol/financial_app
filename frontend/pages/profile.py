"""User profile. Datos reales del backend (/auth/me + /dashboard + /goals).
Stats transaccionales: streak, total expenses, goals count, member since.
"""

from datetime import datetime

from nicegui import ui

import api
import state
import theme
from layout import app_shell, card, require_auth, section


@ui.page("/profile")
async def profile_page():
    if not require_auth():
        return

    with app_shell(active="/profile"):
        with section(top=22):
            ui.label("Profile").style(
                f"color: {theme.PRIMARY}; font-size: 24px; font-weight: 800;"
            )

        with section(top=8):
            with card():
                with ui.row().classes("w-full items-center gap-3"):
                    with ui.element("div").style(
                        f"background: {theme.GREY_BG}; width: 64px; height: 64px; "
                        "border-radius: 50%; display: flex; align-items: center; "
                        "justify-content: center;"
                    ):
                        ui.icon("person").style(
                            f"color: {theme.SECONDARY}; font-size: 36px;"
                        )
                    with ui.column().classes("flex-1 gap-0").style("min-width: 0;"):
                        name_label = ui.label("Loading...").style(
                            f"color: {theme.PRIMARY}; font-size: 17px; font-weight: 700;"
                        )
                        email_label = ui.label("").style(
                            f"color: {theme.GREY_TEXT}; font-size: 12px;"
                        )
                        member_label = ui.label("").style(
                            f"color: {theme.GREY_SOFT}; font-size: 11px;"
                        )

        # Stats: streak | expenses | goals
        with section("Your activity"):
            stats_row = ui.row().classes("w-full gap-2 no-wrap")
            with stats_row:
                streak_card = _make_stat_card("Streak", "0", "local_fire_department", theme.WARNING)
                expenses_card = _make_stat_card(
                    "Expenses", "0", "receipt_long", theme.SECONDARY
                )
                goals_card = _make_stat_card("Goals", "0", "flag", theme.ACCENT)

        # Logout button
        with section(top=18):
            ui.button(
                "Log out", icon="logout", on_click=_logout
            ).props("unelevated no-caps rounded").classes("w-full").style(
                f"background-color: {theme.ERROR}; color: white; height: 48px; font-weight: 600;"
            )
            ui.element("div").style("height: 16px;")

        # --- Cargar datos reales ---
        try:
            me = await api.get_me()
            dashboard = await api.get_dashboard()
            goals = await api.get_goals()
        except api.ApiException as e:
            if e.status in (401, 403):
                ui.navigate.to("/login")
                return
            ui.notify(f"Error: {e.message}", type="negative")
            return

        name_label.text = f"{me['name']} {me['surname']}"
        email_label.text = me["email"]
        try:
            created = datetime.fromisoformat(me["created_at"].replace("Z", "+00:00"))
            member_label.text = f"Member since {created.strftime('%b %Y')}"
        except (ValueError, KeyError):
            member_label.text = ""

        streak_card["value"].text = str(dashboard.get("streak", 0))
        expenses_card["value"].text = str(dashboard.get("total_expenses", 0))
        goals_card["value"].text = str(len(goals))


def _make_stat_card(label: str, value: str, icon: str, color: str) -> dict:
    with ui.column().classes("flex-1 gap-1").style(
        f"background: {theme.WHITE}; border-radius: 14px; padding: 14px; "
        "box-shadow: 0 2px 8px rgba(0,0,0,0.04); align-items: center;"
    ):
        ui.icon(icon).style(f"color: {color}; font-size: 22px;")
        value_label = ui.label(value).style(
            f"color: {theme.PRIMARY}; font-size: 22px; font-weight: 800;"
        )
        ui.label(label).style(
            f"color: {theme.GREY_TEXT}; font-size: 11px; font-weight: 600; "
            "text-transform: uppercase; letter-spacing: 0.5px;"
        )
    return {"value": value_label}


def _logout() -> None:
    state.clear_auth()
    ui.navigate.to("/login")

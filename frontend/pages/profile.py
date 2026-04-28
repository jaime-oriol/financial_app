"""User profile. Datos reales de /auth/me, /dashboard, /goals (en paralelo).
Stats transaccionales: streak, total expenses, goals count, member since.
"""

import asyncio
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

    refs: dict = {}

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
                        refs["name"] = ui.label("Loading...").style(
                            f"color: {theme.PRIMARY}; font-size: 17px; font-weight: 700;"
                        )
                        refs["email"] = ui.label("").style(
                            f"color: {theme.GREY_TEXT}; font-size: 12px;"
                        )
                        refs["member"] = ui.label("").style(
                            f"color: {theme.GREY_SOFT}; font-size: 11px;"
                        )

        with section("Your activity"):
            with ui.row().classes("w-full gap-2 no-wrap"):
                refs["streak"] = _stat_card(
                    "Streak", "0", "local_fire_department", theme.WARNING
                )
                refs["xp"] = _stat_card("XP", "0", "auto_awesome", theme.SECONDARY)
                refs["expenses"] = _stat_card(
                    "Expenses", "0", "receipt_long", theme.PRIMARY
                )
                refs["goals"] = _stat_card("Goals", "0", "flag", theme.ACCENT)

        with section("Achievements"):
            refs["achievements"] = ui.row().classes("w-full gap-2 flex-wrap")

        with section(top=18):
            ui.button(
                "Log out", icon="logout", on_click=_logout
            ).props("unelevated no-caps rounded").classes("w-full").style(
                f"background-color: {theme.ERROR}; color: white; "
                "height: 48px; font-weight: 600;"
            )
            ui.element("div").style("height: 16px;")

    # 3 endpoints en paralelo (3x mas rapido vs secuencial)
    try:
        me, dashboard, goals = await asyncio.gather(
            api.get_me(), api.get_dashboard(), api.get_goals()
        )
    except api.ApiException as e:
        if e.status in (401, 403):
            ui.navigate.to("/login")
            return
        ui.notify(f"Error: {e.message}", type="negative")
        return

    refs["name"].text = f"{me['name']} {me['surname']}"
    refs["email"].text = me["email"]
    try:
        created = datetime.fromisoformat(me["created_at"].replace("Z", "+00:00"))
        refs["member"].text = f"Member since {created.strftime('%b %Y')}"
    except (ValueError, KeyError):
        refs["member"].text = ""

    refs["streak"].text = str(dashboard.get("streak", 0))
    refs["xp"].text = str(dashboard.get("total_xp", 0))
    refs["expenses"].text = str(dashboard.get("total_expenses", 0))
    refs["goals"].text = str(len(goals))

    _render_achievements(refs["achievements"], dashboard.get("achievements", []))


def _stat_card(label: str, value: str, icon: str, color: str) -> ui.label:
    """Crea un card de stat y devuelve la label del numero (mutable)."""
    with ui.column().classes("flex-1 gap-0").style(
        f"background: {theme.WHITE}; border-radius: 14px; padding: 12px 8px; "
        "box-shadow: 0 2px 8px rgba(0,0,0,0.04); align-items: center; min-width: 0; "
        "transition: box-shadow 0.18s ease;"
    ):
        ui.icon(icon).style(f"color: {color}; font-size: 20px;")
        value_label = ui.label(value).classes("fapp-money").style(
            f"color: {theme.PRIMARY}; font-size: 19px; font-weight: 800; margin-top: 4px;"
        )
        ui.label(label).style(
            f"color: {theme.GREY_TEXT}; font-size: 10px; font-weight: 600; "
            "text-transform: uppercase; letter-spacing: 0.5px;"
        )
    return value_label


def _render_achievements(container: ui.row, achievements: list[dict]) -> None:
    """Grid de badges. Cada uno se calcula server-side desde BD."""
    container.clear()
    with container:
        if not achievements:
            ui.label("No achievements yet").style(
                f"color: {theme.GREY_TEXT}; font-size: 12px; padding: 8px 4px;"
            )
            return
        for a in achievements:
            _achievement_chip(a)


def _achievement_chip(a: dict) -> None:
    earned = a["earned"]
    color = a["color"]
    bg = f"{color}1f" if earned else theme.GREY_BG
    icon_color = color if earned else theme.GREY_SOFT
    text_color = theme.PRIMARY if earned else theme.GREY_SOFT
    with ui.column().classes("items-center gap-1").style(
        f"background-color: {bg}; border-radius: 14px; padding: 12px 8px; "
        f"min-width: 88px; flex: 1; "
        f"opacity: {1.0 if earned else 0.6}; transition: transform 0.18s ease;"
    ).tooltip(a["description"]):
        ui.icon(a["icon"]).style(f"color: {icon_color}; font-size: 26px;")
        ui.label(a["name"]).style(
            f"color: {text_color}; font-size: 11px; font-weight: 600; text-align: center;"
        )


def _logout() -> None:
    state.clear_auth()
    ui.navigate.to("/login")

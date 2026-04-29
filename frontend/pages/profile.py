"""User profile. Datos reales de /auth/me, /dashboard, /goals (en paralelo).
Stats transaccionales: streak, total expenses, goals count, member since.
"""

import asyncio
from datetime import datetime

from nicegui import ui

import api
import dialogs
import state
import theme
from layout import app_shell, card, render_avatar, require_auth, section


@ui.page("/profile")
async def profile_page():
    if not require_auth():
        return

    refs: dict = {}

    with app_shell(active="/profile"):
        with section(top=22):
            ui.label("Profile").classes("fapp-page-title")

        async def reload_profile() -> None:
            try:
                me = await api.get_me()
            except api.ApiException:
                return
            refs["current_user"] = me
            render_avatar(refs["avatar_inner"], me, size=64, font_size=28)
            refs["name"].text = f"{me['name']} {me['surname']}"

        with section(top=8):
            with card():
                with ui.row().classes("w-full items-center gap-3"):
                    # Avatar wrapper (clickable, con badge de edit)
                    avatar_wrapper = ui.element("div").classes(
                        "cursor-pointer relative"
                    ).style("width: 64px; height: 64px;").tooltip("Tap to change photo")
                    avatar_wrapper.on(
                        "click",
                        lambda: dialogs.show_avatar_picker(
                            (refs.get("current_user") or {}).get("avatar"),
                            on_success=reload_profile,
                        ),
                    )
                    with avatar_wrapper:
                        refs["avatar_inner"] = ui.element("div").classes(
                            "absolute inset-0"
                        )
                        # Placeholder hasta que llegue /me
                        with refs["avatar_inner"]:
                            ui.element("div").style(
                                f"width: 64px; height: 64px; border-radius: 50%; "
                                f"background: {theme.GREY_BG};"
                            )
                        # Pencil badge en esquina
                        with ui.element("div").style(
                            f"position: absolute; bottom: -2px; right: -2px; "
                            f"background: {theme.SECONDARY}; color: white; "
                            "width: 24px; height: 24px; border-radius: 50%; "
                            "display: flex; align-items: center; justify-content: center; "
                            "border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.15);"
                        ):
                            ui.icon("photo_camera").style(
                                "color: white; font-size: 12px;"
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

        with section("Activity"):
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
                "Sign Out", icon="logout", on_click=_logout
            ).props("unelevated no-caps rounded").classes("w-full").style(
                f"background-color: {theme.ERROR}; color: white; "
                "height: 48px; font-weight: 600; font-size: 14px;"
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

    refs["current_user"] = me
    render_avatar(refs["avatar_inner"], me, size=64, font_size=28)
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
    with ui.column().classes("flex-1 gap-1").style(
        f"background: {theme.WHITE}; border-radius: 18px; padding: 16px 8px; "
        "border: 1px solid rgba(22,33,62,0.07); "
        "box-shadow: 0 1px 2px rgba(22,33,62,0.04), 0 4px 14px rgba(22,33,62,0.07); "
        "align-items: center; min-width: 0;"
    ):
        with ui.element("div").style(
            f"background: {color}18; width: 34px; height: 34px; border-radius: 10px; "
            "display: flex; align-items: center; justify-content: center;"
        ):
            ui.icon(icon).style(f"color: {color}; font-size: 18px;")
        value_label = ui.label(value).classes("fapp-money").style(
            f"color: {theme.PRIMARY}; font-size: 20px; font-weight: 800; line-height: 1;"
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
            ui.label("No achievements earned yet").style(
                f"color: {theme.GREY_TEXT}; font-size: 12px; font-weight: 500; padding: 8px 4px;"
            )
            ui.label("Keep using FAPP to unlock badges.").style(
                f"color: {theme.GREY_SOFT}; font-size: 11px; padding: 0 4px 8px 4px;"
            )
            return
        for a in achievements:
            _achievement_chip(a)


def _achievement_chip(a: dict) -> None:
    earned = a["earned"]
    color = a["color"]
    bg = f"{color}18" if earned else theme.GREY_BG
    border = f"1px solid {color}30" if earned else "1px solid rgba(22,33,62,0.06)"
    icon_color = color if earned else theme.GREY_SOFT
    text_color = theme.PRIMARY if earned else theme.GREY_SOFT
    with ui.column().classes("items-center gap-1").style(
        f"background-color: {bg}; border-radius: 16px; padding: 14px 8px; "
        f"border: {border}; "
        f"min-width: 88px; flex: 1; "
        f"opacity: {1.0 if earned else 0.5}; transition: transform 0.2s ease, opacity 0.2s ease;"
    ).tooltip(a["description"]):
        icon_bg = f"{color}22" if earned else theme.GREY_BG
        with ui.element("div").style(
            f"background: {icon_bg}; "
            "width: 38px; height: 38px; border-radius: 12px; "
            "display: flex; align-items: center; justify-content: center;"
        ):
            ui.icon(a["icon"]).style(f"color: {icon_color}; font-size: 22px;")
        ui.label(a["name"]).style(
            f"color: {text_color}; font-size: 10.5px; font-weight: 700; "
            "text-align: center; letter-spacing: 0.1px;"
        )


def _logout() -> None:
    state.clear_auth()
    ui.navigate.to("/login")

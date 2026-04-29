"""Savings Goals. Aplica feedback clave del profesor: goals 100% transaccionales
con botones +/- (Add money / Withdraw). Diálogos compartidos en dialogs.py.
"""

from datetime import date

from nicegui import ui

import api
import dialogs
import theme
from layout import (
    app_shell,
    card,
    empty_state,
    primary_button,
    require_auth,
    section,
)


@ui.page("/goals")
async def goals_page():
    if not require_auth():
        return

    refs: dict = {}

    async def reload() -> None:
        try:
            goals = await api.get_goals()
        except api.ApiException as e:
            if e.status in (401, 403):
                ui.navigate.to("/login")
                return
            ui.notify(f"Error: {e.message}", type="negative")
            return

        refs["list"].clear()
        with refs["list"]:
            if not goals:
                with card():
                    empty_state("flag", "No goals yet. Set your first savings goal!")
                return
            for g in goals:
                _goal_card(g, reload)

    with app_shell(active="/goals"):
        with section(top=22):
            ui.label("Goals").style(
                f"color: {theme.PRIMARY}; font-size: 24px; font-weight: 800;"
            )
            ui.label("Set savings goals and track your progress").style(
                f"color: {theme.GREY_TEXT}; font-size: 13px;"
            )

        with section():
            refs["list"] = ui.column().classes("w-full gap-3")

        with section():
            primary_button(
                "New goal",
                lambda: dialogs.show_create_goal(on_success=reload),
                icon="add",
            )
            ui.element("div").style("height: 16px;")

    await reload()


def _goal_card(goal: dict, reload) -> None:
    progress_pct = float(goal["progress"])
    progress = progress_pct / 100
    is_complete = progress >= 1.0
    is_behind = _is_behind_pace(goal) and not is_complete

    bar_color = (
        theme.ACCENT if is_complete else (theme.WARNING if is_behind else theme.SECONDARY)
    )
    badge_text = "Completed" if is_complete else ("Behind" if is_behind else "On track")

    async def do_delete() -> None:
        await api.delete_goal(goal["goal_id"])
        ui.notify("Goal deleted", type="positive")
        await reload()

    with ui.column().classes("w-full gap-3").style(
        f"background: {theme.WHITE}; border-radius: 20px; padding: 20px; "
        "box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 6px 20px rgba(0,0,0,0.05);"
    ):
        # Header: nombre + status + delete
        with ui.row().classes("w-full items-center no-wrap gap-2"):
            ui.label(goal["name"]).classes("flex-1").style(
                f"color: {theme.PRIMARY}; font-size: 16px; font-weight: 700;"
            )
            ui.label(badge_text).style(
                f"background-color: {bar_color}26; color: {bar_color}; "
                "padding: 3px 10px; border-radius: 8px; font-size: 11px; "
                "font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;"
            )
            ui.button(icon="delete_outline").props("flat dense round size=sm").style(
                f"color: {theme.GREY_SOFT};"
            ).on(
                "click",
                lambda: dialogs.show_confirm(
                    f"Delete \"{goal['name']}\"?", do_delete
                ),
            )

        ui.label(theme.fmt_money(goal["saved_amount"])).classes("fapp-money").style(
            f"color: {theme.PRIMARY}; font-size: 26px; font-weight: 800;"
        )
        ui.label(f"of {theme.fmt_money(goal['target_amount'], 0)} goal").style(
            f"color: {theme.GREY_TEXT}; font-size: 12px; margin-top: -6px;"
        )

        ui.linear_progress(value=min(progress, 1.0), show_value=False, size="10px").props(
            "rounded"
        ).style(f"--q-primary: {bar_color};")

        with ui.row().classes("w-full justify-between items-center"):
            ui.label(f"{progress_pct:.0f}% saved").style(
                f"color: {theme.PRIMARY}; font-size: 12px; font-weight: 600;"
            )
            if goal.get("deadline"):
                ui.label(f"Target: {goal['deadline']}").style(
                    f"color: {theme.GREY_TEXT}; font-size: 12px;"
                )

        if is_behind:
            with ui.row().classes("w-full items-center gap-2 no-wrap").style(
                f"background-color: {theme.WARNING}1a; border-radius: 8px; padding: 8px;"
            ):
                ui.icon("info_outline").style(
                    f"color: {theme.WARNING}; font-size: 16px;"
                )
                ui.label(_pace_message(goal)).style(
                    f"color: {theme.WARNING}; font-size: 12px;"
                )

        # Botones +/- — feedback CLAVE del profesor (goals transaccionales)
        with ui.row().classes("w-full gap-2 no-wrap").style("margin-top: 4px;"):
            ui.button(
                "Add money",
                icon="add",
                on_click=lambda: dialogs.show_contribute_goal(
                    goal["goal_id"], +1, on_success=reload
                ),
            ).props("unelevated no-caps rounded").classes("flex-1").style(
                f"background-color: {theme.SECONDARY}; color: white; height: 40px;"
            )
            ui.button(
                "Withdraw",
                icon="remove",
                on_click=lambda: dialogs.show_contribute_goal(
                    goal["goal_id"], -1, on_success=reload
                ),
            ).props("outline no-caps rounded").classes("flex-1").style(
                f"color: {theme.SECONDARY}; height: 40px; border-color: {theme.SECONDARY};"
            )


def _is_behind_pace(goal: dict) -> bool:
    if not goal.get("deadline"):
        return False
    try:
        deadline = date.fromisoformat(goal["deadline"])
        created = date.fromisoformat(goal["created_at"][:10])
    except (ValueError, TypeError, KeyError):
        return False
    today = date.today()
    if today >= deadline:
        return False
    total_days = max((deadline - created).days, 1)
    elapsed = max((today - created).days, 0)
    expected = elapsed / total_days
    actual = float(goal["progress"]) / 100
    return actual < expected * 0.85


def _pace_message(goal: dict) -> str:
    try:
        deadline = date.fromisoformat(goal["deadline"])
    except (ValueError, TypeError, KeyError):
        return "Save more to stay on track"
    today = date.today()
    days_left = max((deadline - today).days, 1)
    remaining = float(goal["target_amount"]) - float(goal["saved_amount"])
    if remaining <= 0:
        return "Goal reached!"
    weekly = remaining / max(days_left / 7, 1)
    return f"Save ~{theme.fmt_money(weekly, 0)}/week to reach your goal on time"

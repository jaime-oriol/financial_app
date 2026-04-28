"""Savings Goals. Aplica feedback del profesor: goals 100% transaccionales con
botones +/- para meter/sacar dinero. Nada hardcoded.
Backend: POST /goals, GET /goals, POST /goals/{id}/contribute, DELETE /goals/{id}.
"""

from datetime import date

from nicegui import ui

import api
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
                "New goal", lambda: _create_goal_dialog(refs), icon="add"
            )
            ui.element("div").style("height: 16px;")

        await _reload(refs)


async def _reload(refs: dict) -> None:
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
                empty_state(
                    "flag",
                    "No goals yet. Set your first savings goal!",
                )
            return
        for g in goals:
            _goal_card(g, refs)


def _goal_card(goal: dict, refs: dict) -> None:
    progress = goal["progress"] / 100
    is_complete = progress >= 1.0
    is_behind = _is_behind_pace(goal) and not is_complete

    bar_color = theme.ACCENT if is_complete else (theme.WARNING if is_behind else theme.SECONDARY)
    badge_text = "Completed" if is_complete else ("Behind" if is_behind else "On track")
    badge_color = bar_color

    with ui.column().classes("w-full gap-3").style(
        f"background: {theme.WHITE}; border-radius: 16px; padding: 18px; "
        "box-shadow: 0 2px 8px rgba(0,0,0,0.04);"
    ):
        # Header: name + status badge + delete
        with ui.row().classes("w-full items-center no-wrap gap-2"):
            ui.label(goal["name"]).classes("flex-1").style(
                f"color: {theme.PRIMARY}; font-size: 16px; font-weight: 700;"
            )
            ui.label(badge_text).style(
                f"background-color: {badge_color}26; color: {badge_color}; "
                "padding: 3px 10px; border-radius: 8px; font-size: 11px; "
                "font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;"
            )
            ui.button(icon="more_vert").props("flat dense round size=sm").style(
                f"color: {theme.GREY_SOFT};"
            ).on("click", lambda gid=goal["goal_id"]: _confirm_delete_goal(gid, refs))

        # Saved / target
        ui.label(theme.fmt_money(goal["saved_amount"])).style(
            f"color: {theme.PRIMARY}; font-size: 26px; font-weight: 800;"
        )
        ui.label(f"of {theme.fmt_money(goal['target_amount'], 0)} goal").style(
            f"color: {theme.GREY_TEXT}; font-size: 12px; margin-top: -6px;"
        )

        # Progress bar
        ui.linear_progress(value=min(progress, 1.0), show_value=False, size="10px").props(
            "rounded"
        ).style(f"--q-primary: {bar_color};")

        # Info row
        with ui.row().classes("w-full justify-between items-center"):
            ui.label(f"{goal['progress']:.0f}% saved").style(
                f"color: {theme.PRIMARY}; font-size: 12px; font-weight: 600;"
            )
            if goal.get("deadline"):
                ui.label(f"Target: {goal['deadline']}").style(
                    f"color: {theme.GREY_TEXT}; font-size: 12px;"
                )

        # Behind-pace warning (transaccional: deriva de saved_amount, target, deadline)
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

        # Botones +/- — el feedback CLAVE del profesor
        with ui.row().classes("w-full gap-2 no-wrap").style("margin-top: 4px;"):
            ui.button(
                "Add money",
                icon="add",
                on_click=lambda gid=goal["goal_id"]: _contribute_dialog(gid, refs, sign=+1),
            ).props("unelevated no-caps rounded").classes("flex-1").style(
                f"background-color: {theme.SECONDARY}; color: white; height: 40px;"
            )
            ui.button(
                "Withdraw",
                icon="remove",
                on_click=lambda gid=goal["goal_id"]: _contribute_dialog(gid, refs, sign=-1),
            ).props("outline no-caps rounded").classes("flex-1").style(
                f"color: {theme.SECONDARY}; height: 40px; border-color: {theme.SECONDARY};"
            )


def _is_behind_pace(goal: dict) -> bool:
    """Detecta si el ritmo de ahorro va lento dado el deadline."""
    if not goal.get("deadline"):
        return False
    try:
        deadline = date.fromisoformat(goal["deadline"])
    except (ValueError, TypeError):
        return False

    created = date.fromisoformat(goal["created_at"][:10])
    today = date.today()
    total_days = max((deadline - created).days, 1)
    elapsed = max((today - created).days, 0)
    expected_progress = elapsed / total_days  # fraccion de tiempo transcurrido
    actual_progress = goal["progress"] / 100
    return today < deadline and actual_progress < expected_progress * 0.85


def _pace_message(goal: dict) -> str:
    try:
        deadline = date.fromisoformat(goal["deadline"])
    except (ValueError, TypeError):
        return "Save more to stay on track"
    today = date.today()
    days_left = max((deadline - today).days, 1)
    remaining = float(goal["target_amount"]) - float(goal["saved_amount"])
    if remaining <= 0:
        return "Goal reached!"
    weekly = remaining / max(days_left / 7, 1)
    return f"Save ~{theme.fmt_money(weekly, 0)}/week to reach your goal on time"


# --- Dialogos ---

def _contribute_dialog(goal_id: int, refs: dict, sign: int) -> None:
    title = "Add money" if sign > 0 else "Withdraw"
    quick_amounts = [5, 10, 25, 50] if sign > 0 else [5, 10, 25]

    with ui.dialog() as dialog, ui.card().style(
        f"width: 320px; border-radius: 16px; padding: 20px; background: {theme.WHITE};"
    ):
        ui.label(title).style(
            f"color: {theme.PRIMARY}; font-size: 18px; font-weight: 700;"
        )

        amount = ui.number("Amount", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full")

        with ui.row().classes("w-full gap-2 flex-wrap").style("margin-top: 4px;"):
            ui.label("Quick:").style(
                f"color: {theme.GREY_TEXT}; font-size: 12px; align-self: center;"
            )
            for q in quick_amounts:
                ui.button(f"${q}", on_click=lambda v=q: setattr(amount, "value", float(v))).props(
                    "outline dense no-caps rounded"
                ).style(
                    f"color: {theme.SECONDARY}; border-color: {theme.SECONDARY}; "
                    "min-width: 0; padding: 4px 12px;"
                )

        async def submit():
            if not amount.value or amount.value <= 0:
                ui.notify("Amount must be greater than 0", type="warning")
                return
            try:
                await api.contribute_goal(goal_id, sign * float(amount.value))
                dialog.close()
                ui.notify(
                    f"{'Added' if sign > 0 else 'Withdrew'} {theme.fmt_money(amount.value)}",
                    type="positive",
                )
                await _reload(refs)
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        with ui.row().classes("w-full justify-end gap-2").style("margin-top: 14px;"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps").style(
                f"color: {theme.GREY_TEXT};"
            )
            ui.button(
                "Confirm", on_click=submit
            ).props("unelevated no-caps").style(
                f"background-color: {theme.SECONDARY}; color: white;"
            )

    dialog.open()


def _create_goal_dialog(refs: dict) -> None:
    with ui.dialog() as dialog, ui.card().style(
        f"width: 360px; border-radius: 16px; padding: 22px; background: {theme.WHITE};"
    ):
        ui.label("New savings goal").style(
            f"color: {theme.PRIMARY}; font-size: 18px; font-weight: 700;"
        )
        name = ui.input("What are you saving for?").props(
            "outlined dense"
        ).classes("w-full")
        target = ui.number("Target amount", value=None, format="%.2f", min=0.01).props(
            "outlined dense prefix=$"
        ).classes("w-full")

        d = ui.input("Deadline (optional)", value="").props(
            "outlined dense readonly clearable"
        ).classes("w-full")
        with d.add_slot("append"):
            ui.icon("event").classes("cursor-pointer").on(
                "click", lambda: date_dialog.open()
            )
        with ui.dialog() as date_dialog, ui.card():
            ui.date(on_change=lambda e: setattr(d, "value", e.value or "")).props(
                "mask=YYYY-MM-DD"
            )
            ui.button("OK", on_click=date_dialog.close).props("flat")

        async def submit():
            if not name.value or not name.value.strip():
                ui.notify("Name is required", type="warning")
                return
            if not target.value or target.value <= 0:
                ui.notify("Target must be greater than 0", type="warning")
                return
            try:
                await api.create_goal(
                    name.value.strip(),
                    float(target.value),
                    d.value if d.value else None,
                )
                dialog.close()
                ui.notify("Goal created", type="positive")
                await _reload(refs)
            except api.ApiException as e:
                ui.notify(f"Error: {e.message}", type="negative")

        with ui.row().classes("w-full justify-end gap-2").style("margin-top: 14px;"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps").style(
                f"color: {theme.GREY_TEXT};"
            )
            ui.button("Create", on_click=submit).props("unelevated no-caps").style(
                f"background-color: {theme.SECONDARY}; color: white;"
            )

    dialog.open()


def _confirm_delete_goal(goal_id: int, refs: dict) -> None:
    with ui.dialog() as dialog, ui.card().style(
        "border-radius: 14px; padding: 18px; min-width: 280px;"
    ):
        ui.label("Delete this goal?").style(
            f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 600;"
        )
        ui.label("This action cannot be undone.").style(
            f"color: {theme.GREY_TEXT}; font-size: 12px;"
        )
        with ui.row().classes("w-full justify-end gap-2").style("margin-top: 8px;"):
            ui.button("Cancel", on_click=dialog.close).props("flat no-caps")

            async def go():
                try:
                    await api.delete_goal(goal_id)
                    dialog.close()
                    ui.notify("Goal deleted", type="positive")
                    await _reload(refs)
                except api.ApiException as e:
                    ui.notify(f"Error: {e.message}", type="negative")

            ui.button("Delete", on_click=go).props("unelevated no-caps").style(
                f"background-color: {theme.ERROR}; color: white;"
            )
    dialog.open()

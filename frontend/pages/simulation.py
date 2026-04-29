"""Simulation transaccional. Carga el reto desde /api/challenges (datos en BD),
muestra escenario + opciones, y al confirmar POSTea {choice_idx} a
/challenges/{id}/attempt. El XP se calcula server-side por la opcion elegida.
"""

from nicegui import ui

import api
import theme
from layout import card, page_setup, primary_button, require_auth


_TAG_COLOR = {
    "Risky": theme.ERROR,
    "Smart": theme.ACCENT,
    "Not ideal": theme.WARNING,
}


@ui.page("/simulation/{challenge_id}")
async def simulation_page(challenge_id: int):
    if not require_auth():
        return

    page_setup("Simulation")
    ui.query("body").style(f"background-color: {theme.BG};")

    try:
        all_challenges = await api.get_challenges()
    except api.ApiException as e:
        if e.status in (401, 403):
            ui.navigate.to("/login")
            return
        ui.notify(f"Error: {e.message}", type="negative")
        return

    challenge = next(
        (c for c in all_challenges if c["challenge_id"] == challenge_id and c["kind"] == "simulation"),
        None,
    )
    if not challenge:
        ui.label("Challenge not found").style(f"color: {theme.ERROR}; padding: 20px;")
        return

    content = challenge["content"]
    choices = content["choices"]
    state = {"selected": None, "submitting": False}

    with ui.row().classes("w-full max-w-[480px] mx-auto items-center gap-2").style(
        f"background: {theme.WHITE}; padding: 14px 16px; "
        "border-bottom: 1px solid rgba(22,33,62,0.07); "
        "box-shadow: 0 1px 8px rgba(22,33,62,0.05);"
    ):
        ui.button(icon="arrow_back").props("flat dense round").on(
            "click", lambda: ui.navigate.to("/challenges")
        ).style(f"color: {theme.PRIMARY};")
        ui.label(challenge["title"]).classes("flex-1").style(
            f"color: {theme.PRIMARY}; font-size: 16px; font-weight: 700;"
        )

    body = ui.column().classes("w-full max-w-[480px] mx-auto gap-3").style(
        "padding: 18px 16px;"
    )

    def _scenario_card() -> None:
        with card():
            with ui.row().classes("w-full items-center gap-3 no-wrap"):
                with ui.element("div").style(
                    f"background: {theme.SECONDARY}1a; width: 44px; height: 44px; "
                    "border-radius: 12px; display: flex; align-items: center; justify-content: center;"
                ):
                    ui.icon("psychology").style(
                        f"color: {theme.SECONDARY}; font-size: 22px;"
                    )
                ui.label(challenge["title"]).style(
                    f"color: {theme.PRIMARY}; font-size: 17px; font-weight: 700;"
                )
            ui.label(content["scenario"]).style(
                f"color: {theme.PRIMARY}; font-size: 14px; line-height: 1.5; margin-top: 4px;"
            )
            with ui.row().classes("w-full items-center justify-between gap-2 no-wrap").style(
                f"background-color: {theme.GREY_BG}; border-radius: 10px; padding: 12px; margin-top: 6px;"
            ):
                ui.label("Available").style(f"color: {theme.GREY_TEXT}; font-size: 11px;")
                ui.label(f"${content.get('budget', 0):.0f}").classes("fapp-money").style(
                    f"color: {theme.PRIMARY}; font-size: 18px; font-weight: 800;"
                )
                ui.label(content.get("categories_label", "")).style(
                    f"color: {theme.GREY_TEXT}; font-size: 11px;"
                )

    def render_choices() -> None:
        body.clear()
        with body:
            _scenario_card()
            ui.label("Choose your approach").style(
                f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 700; "
                "letter-spacing: -0.2px; margin-top: 4px;"
            )

            chips = []
            for i, c in enumerate(choices):
                tag_color = _TAG_COLOR.get(c["tag"], theme.SECONDARY)
                chip = _choice_card(i, c, tag_color)
                chips.append((chip, tag_color))

            confirm_btn = primary_button("Confirm Choice", _confirm)
            confirm_btn.disable()

            def select(idx: int) -> None:
                state["selected"] = idx
                for i, (chip, tag_color) in enumerate(chips):
                    is_sel = i == idx
                    chip.style(
                        f"background-color: {theme.WHITE}; "
                        f"border: 2px solid {tag_color if is_sel else 'transparent'}; "
                        f"border-radius: 14px; padding: 14px; "
                        f"box-shadow: 0 2px 8px rgba(0,0,0,{'0.10' if is_sel else '0.04'});"
                    )
                confirm_btn.enable()

            for i, (chip, _) in enumerate(chips):
                chip.on("click", lambda i=i: select(i))

    def _choice_card(idx: int, c: dict, tag_color: str) -> ui.element:
        chip = ui.column().classes("w-full gap-1 cursor-pointer").style(
            f"background-color: {theme.WHITE}; border: 1.5px solid rgba(22,33,62,0.08); "
            "border-radius: 16px; padding: 16px; "
            "box-shadow: 0 1px 2px rgba(22,33,62,0.04), 0 2px 8px rgba(22,33,62,0.05); "
            "transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.15s ease;"
        )
        with chip:
            with ui.row().classes("w-full items-center justify-between no-wrap"):
                ui.label(c["label"]).classes("flex-1").style(
                    f"color: {theme.PRIMARY}; font-size: 14px; font-weight: 600;"
                )
                ui.label(c["tag"]).style(
                    f"background-color: {tag_color}26; color: {tag_color}; "
                    "padding: 3px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; "
                    "letter-spacing: 0.5px; text-transform: uppercase;"
                )
            ui.label(c["split"]).style(
                f"color: {theme.GREY_TEXT}; font-size: 12px;"
            )
        return chip

    async def _confirm() -> None:
        if state["selected"] is None or state["submitting"]:
            return
        state["submitting"] = True
        try:
            attempt = await api.submit_attempt(
                challenge_id, {"choice_idx": state["selected"]}
            )
            _render_outcome(attempt)
        except api.ApiException as e:
            ui.notify(f"Error: {e.message}", type="negative")
            state["submitting"] = False

    def _render_outcome(attempt: dict) -> None:
        body.clear()
        c = choices[state["selected"]]
        tag_color = _TAG_COLOR.get(c["tag"], theme.SECONDARY)
        xp = attempt.get("xp_earned", 0)
        with body:
            _scenario_card()
            ui.label("Result").style(
                f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 700; "
                "letter-spacing: -0.2px; margin-top: 4px;"
            )
            with card():
                with ui.row().classes("w-full items-center gap-2 no-wrap"):
                    ui.icon(
                        "check_circle" if c["savings"] >= 70 else "warning_amber"
                    ).style(f"color: {tag_color}; font-size: 22px;")
                    ui.label(c["tag"]).style(
                        f"color: {tag_color}; font-size: 16px; font-weight: 700;"
                    )
                ui.label(c["outcome"]).style(
                    f"color: {theme.PRIMARY}; font-size: 14px; line-height: 1.5;"
                )
                with ui.row().classes("w-full items-center justify-between gap-2 no-wrap").style(
                    f"background-color: {tag_color}1a; border-radius: 10px; padding: 12px; margin-top: 6px;"
                ):
                    ui.label("Savings this month").style(
                        f"color: {theme.GREY_TEXT}; font-size: 12px;"
                    )
                    ui.label(f"${c['savings']:.0f}").classes("fapp-money").style(
                        f"color: {tag_color}; font-size: 17px; font-weight: 800;"
                    )
                with ui.row().classes("w-full items-center gap-1").style("margin-top: 4px;"):
                    ui.icon("auto_awesome").style(
                        f"color: {theme.SECONDARY}; font-size: 18px;"
                    )
                    ui.label(f"+{xp} XP earned").style(
                        f"color: {theme.SECONDARY}; font-size: 14px; font-weight: 700;"
                    )

            with ui.row().classes("w-full gap-2 no-wrap"):
                ui.button("Retry", on_click=lambda: _retry()).props(
                    "outline no-caps rounded"
                ).classes("flex-1").style(
                    f"color: {theme.SECONDARY}; height: 46px; border-color: {theme.SECONDARY}; font-weight: 600;"
                )
                ui.button(
                    "Back to Challenges", on_click=lambda: ui.navigate.to("/challenges")
                ).props("unelevated no-caps rounded").classes("flex-1").style(
                    f"background-color: {theme.SECONDARY}; color: {theme.WHITE}; height: 46px; font-weight: 600;"
                )

    def _retry() -> None:
        state["selected"] = None
        state["submitting"] = False
        render_choices()

    render_choices()

"""Quiz transaccional. Carga el reto desde /api/challenges (datos en BD),
muestra preguntas, y al final POSTea {score, total} a /challenges/{id}/attempt
para que se almacene y el XP del usuario se actualice.
"""

from nicegui import ui

import api
import theme
from layout import card, page_setup, primary_button, require_auth


@ui.page("/quiz/{challenge_id}")
async def quiz_page(challenge_id: int):
    if not require_auth():
        return

    page_setup("Quiz")
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
        (c for c in all_challenges if c["challenge_id"] == challenge_id and c["kind"] == "quiz"),
        None,
    )
    if not challenge:
        ui.label("Challenge not found").style(f"color: {theme.ERROR}; padding: 20px;")
        return

    questions = challenge["content"]["questions"]
    state = {"index": 0, "selected": None, "answered": False, "score": 0, "submitting": False}

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
        score_badge = ui.label("0 XP").style(
            f"background-color: {theme.SECONDARY}; color: {theme.WHITE}; "
            "padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 700;"
        )

    body = ui.column().classes("w-full max-w-[480px] mx-auto gap-3").style(
        "padding: 18px 16px;"
    )

    def render_question() -> None:
        body.clear()
        q = questions[state["index"]]
        with body:
            ui.label(f"Question {state['index'] + 1} of {len(questions)}").style(
                f"color: {theme.GREY_TEXT}; font-size: 11px; font-weight: 600; "
                "letter-spacing: 1px; text-transform: uppercase;"
            )
            ui.linear_progress(
                value=(state["index"] + 1) / len(questions), show_value=False, size="6px"
            ).props("rounded").style(f"--q-primary: {theme.SECONDARY};")
            with card():
                ui.label(q["question"]).style(
                    f"color: {theme.PRIMARY}; font-size: 16px; font-weight: 600;"
                )
            options_col = ui.column().classes("w-full gap-2")
            with options_col:
                option_chips = []
                for i, opt in enumerate(q["options"]):
                    chip = _option_button(i, opt)
                    option_chips.append(chip)

            def select(idx: int) -> None:
                if state["answered"]:
                    return
                state["selected"] = idx
                state["answered"] = True
                if idx == q["correct"]:
                    state["score"] += 1
                    score_badge.text = f"{state['score'] * 10} XP"
                _paint_options(option_chips, q, idx)
                _show_explanation(body, q, idx == q["correct"])
                _show_next_button(body)

            for i, chip in enumerate(option_chips):
                chip.on_click(lambda i=i: select(i))

    def _option_button(idx: int, label: str) -> ui.button:
        btn = ui.button(f"{chr(65 + idx)}.  {label}").props(
            "no-caps unelevated rounded"
        ).classes("w-full justify-start").style(
            f"background-color: {theme.GREY_BG}; color: {theme.PRIMARY}; "
            "border: 1.5px solid rgba(22,33,62,0.09); "
            "padding: 14px 16px; height: auto; "
            "text-align: left; font-weight: 500; font-size: 13.5px; "
            "transition: background-color 0.15s ease, border-color 0.15s ease;"
        )
        return btn

    def _paint_options(chips: list[ui.button], q: dict, selected_idx: int) -> None:
        correct_idx = q["correct"]
        for i, chip in enumerate(chips):
            if i == correct_idx:
                chip.style(
                    f"background-color: {theme.ACCENT}26; color: {theme.ACCENT}; "
                    f"border: 2px solid {theme.ACCENT}; padding: 14px; height: auto; "
                    "text-align: left; font-weight: 600;"
                )
            elif i == selected_idx:
                chip.style(
                    f"background-color: {theme.ERROR}26; color: {theme.ERROR}; "
                    f"border: 2px solid {theme.ERROR}; padding: 14px; height: auto; "
                    "text-align: left; font-weight: 600;"
                )

    def _show_explanation(container: ui.column, q: dict, is_correct: bool) -> None:
        c = theme.ACCENT if is_correct else theme.WARNING
        with container:
            with ui.row().classes("w-full items-start gap-2 no-wrap").style(
                f"background-color: {c}1a; border-radius: 12px; padding: 12px;"
            ):
                ui.icon("lightbulb" if is_correct else "info_outline").style(
                    f"color: {c}; font-size: 18px; margin-top: 2px;"
                )
                ui.label(q["explanation"]).style(
                    f"color: {theme.PRIMARY}; font-size: 13px; line-height: 1.5;"
                )

    def _show_next_button(container: ui.column) -> None:
        last = state["index"] >= len(questions) - 1
        async def go() -> None:
            if last:
                await _submit()
            else:
                state["index"] += 1
                state["selected"] = None
                state["answered"] = False
                render_question()
        with container:
            primary_button("Finish" if last else "Next Question", go)

    async def _submit() -> None:
        if state["submitting"]:
            return
        state["submitting"] = True
        try:
            attempt = await api.submit_attempt(
                challenge_id, {"score": state["score"], "total": len(questions)}
            )
            _show_results(attempt)
        except api.ApiException as e:
            ui.notify(f"Error: {e.message}", type="negative")
            state["submitting"] = False

    def _show_results(attempt: dict) -> None:
        body.clear()
        score = state["score"]
        total = len(questions)
        perfect = score == total
        xp = attempt.get("xp_earned", 0)
        with body:
            with ui.column().classes("w-full items-center gap-2").style("padding: 32px 12px;"):
                with ui.element("div").style(
                    f"background: {theme.WARNING if perfect else theme.SECONDARY}1a; "
                    "width: 80px; height: 80px; border-radius: 24px; "
                    "display: flex; align-items: center; justify-content: center;"
                ):
                    ui.icon("emoji_events" if perfect else "school").style(
                        f"color: {theme.WARNING if perfect else theme.SECONDARY}; font-size: 44px;"
                    )
                ui.label("All correct!" if perfect else "Quiz complete").style(
                    f"color: {theme.PRIMARY}; font-size: 22px; font-weight: 800; "
                    "letter-spacing: -0.5px; margin-top: 4px;"
                )
                ui.label(f"{score} of {total} correct answers").style(
                    f"color: {theme.GREY_TEXT}; font-size: 14px; font-weight: 500;"
                )
                with ui.row().classes("items-center gap-1").style(
                    f"background: {theme.SECONDARY}1a; border-radius: 10px; "
                    "padding: 8px 16px; margin-top: 8px;"
                ):
                    ui.icon("auto_awesome").style(
                        f"color: {theme.SECONDARY}; font-size: 18px;"
                    )
                    ui.label(f"+{xp} XP earned").style(
                        f"color: {theme.SECONDARY}; font-size: 15px; font-weight: 700;"
                    )
                ui.label("Result recorded").style(
                    f"color: {theme.GREY_SOFT}; font-size: 11px; margin-top: 4px;"
                )
            primary_button("Back to Challenges", lambda: ui.navigate.to("/challenges"))

    render_question()

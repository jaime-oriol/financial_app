"""Challenges hub. Lista los retos disponibles (quiz + simulation) con su
estado para el usuario (best XP, completado). Cada card lleva a su pagina.
Todo transaccional: el contenido del reto viene de BD, los intentos se
almacenan en BD via /challenges/{id}/attempt.
"""

from nicegui import ui

import api
import theme
from layout import app_shell, card, empty_state, require_auth, section


KIND_META = {
    "quiz": {"icon": "quiz", "color": theme.WARNING, "subtitle": "Multiple-choice"},
    "simulation": {"icon": "psychology", "color": theme.SECONDARY, "subtitle": "Decision scenario"},
}


@ui.page("/challenges")
async def challenges_page():
    if not require_auth():
        return

    refs: dict = {}

    async def reload() -> None:
        try:
            challenges, dashboard = await _load(refs)
        except api.ApiException as e:
            if e.status in (401, 403):
                ui.navigate.to("/login")
                return
            ui.notify(f"Error: {e.message}", type="negative")
            return

        refs["xp_label"].text = f"{dashboard.get('total_xp', 0)} XP"
        refs["done_label"].text = (
            f"{dashboard.get('challenges_done', 0)} attempt"
            f"{'s' if dashboard.get('challenges_done', 0) != 1 else ''}"
        )
        _render_list(refs["list"], challenges)

    with app_shell(active="/challenges"):
        with section(top=22):
            ui.label("Challenges").style(
                f"color: {theme.PRIMARY}; font-size: 24px; font-weight: 800;"
            )
            ui.label("Earn XP by playing real-world money scenarios").style(
                f"color: {theme.GREY_TEXT}; font-size: 13px;"
            )

        # XP banner
        with section(top=14):
            with ui.row().classes("w-full items-center no-wrap gap-3").style(
                "background: linear-gradient(135deg, #2675E3 0%, #16213E 100%); "
                "border-radius: 16px; padding: 16px;"
            ):
                with ui.element("div").style(
                    "background: rgba(255,255,255,0.16); width: 44px; height: 44px; "
                    "border-radius: 12px; display: flex; align-items: center; justify-content: center;"
                ):
                    ui.icon("auto_awesome").style(f"color: {theme.WHITE}; font-size: 24px;")
                with ui.column().classes("flex-1 gap-0").style("min-width: 0;"):
                    refs["xp_label"] = ui.label("0 XP").classes("fapp-money").style(
                        f"color: {theme.WHITE}; font-size: 22px; font-weight: 800;"
                    )
                    refs["done_label"] = ui.label("0 attempts").style(
                        "color: rgba(255,255,255,0.75); font-size: 12px;"
                    )

        with section("Available challenges"):
            refs["list"] = ui.column().classes("w-full gap-3")
            ui.element("div").style("height: 16px;")

    await reload()


async def _load(_refs):
    import asyncio
    return await asyncio.gather(api.get_challenges(), api.get_dashboard())


def _render_list(container: ui.column, challenges: list[dict]) -> None:
    container.clear()
    with container:
        if not challenges:
            with card():
                empty_state("emoji_events", "No challenges available yet")
            return
        for c in challenges:
            _challenge_card(c)


def _challenge_card(challenge: dict) -> None:
    meta = KIND_META.get(challenge["kind"], {"icon": "emoji_events", "color": theme.SECONDARY, "subtitle": ""})
    color = meta["color"]
    completed = challenge.get("completed", False)
    best = challenge.get("best_xp", 0)
    target_path = f"/{challenge['kind']}/{challenge['challenge_id']}"

    with ui.row().classes("w-full no-wrap items-stretch gap-0 cursor-pointer fapp-card").style(
        "padding: 0; overflow: hidden;"
    ).on("click", lambda p=target_path: ui.navigate.to(p)):
        ui.element("div").style(f"width: 5px; background-color: {color};")
        with ui.row().classes("flex-1 no-wrap items-center gap-3").style("padding: 14px;"):
            with ui.element("div").style(
                f"background: {color}1f; width: 44px; height: 44px; border-radius: 12px; "
                "display: flex; align-items: center; justify-content: center;"
            ):
                ui.icon(meta["icon"]).style(f"color: {color}; font-size: 22px;")
            with ui.column().classes("flex-1 gap-0").style("min-width: 0;"):
                with ui.row().classes("items-center gap-2 no-wrap"):
                    ui.label(challenge["title"]).style(
                        f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 700;"
                    )
                    if completed:
                        ui.label("DONE").style(
                            f"background-color: {theme.ACCENT}26; color: {theme.ACCENT}; "
                            "padding: 2px 8px; border-radius: 6px; font-size: 9.5px; "
                            "font-weight: 700; letter-spacing: 0.5px;"
                        )
                ui.label(meta["subtitle"]).style(
                    f"color: {theme.GREY_TEXT}; font-size: 12px;"
                )
                ui.label(
                    f"Best: {best} XP" if completed else f"Earn up to {challenge['xp_reward']} XP"
                ).style(f"color: {color}; font-size: 11px; font-weight: 600; margin-top: 2px;")
            ui.icon("chevron_right").style(f"color: {theme.GREY_SOFT}; font-size: 22px;")

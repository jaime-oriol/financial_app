"""Challenges hub estilo "menu de niveles". Beginner -> Intermediate -> Advanced.
Cada nivel se desbloquea cuando el usuario completa 3 retos del nivel anterior
(logica server-side en challenge_service.list_with_status).

Todo transaccional: contenido y estado vienen de /api/challenges; los attempts
se guardan en /api/challenges/{id}/attempt.
"""

import asyncio

from nicegui import ui

import api
import theme
from layout import app_shell, card, empty_state, require_auth, section


KIND_META = {
    "quiz": {"icon": "quiz", "subtitle": "Multiple-choice"},
    "simulation": {"icon": "psychology", "subtitle": "Decision scenario"},
}

LEVEL_META = {
    1: {"name": "Beginner", "color": "#27AE60", "icon": "looks_one"},
    2: {"name": "Intermediate", "color": "#2675E3", "icon": "looks_two"},
    3: {"name": "Advanced", "color": "#8E44AD", "icon": "looks_3"},
}

UNLOCK_THRESHOLD = 3


@ui.page("/challenges")
async def challenges_page():
    if not require_auth():
        return

    refs: dict = {}

    async def reload() -> None:
        try:
            challenges, dashboard = await asyncio.gather(
                api.get_challenges(), api.get_dashboard()
            )
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
        _render_levels(refs["list"], challenges)

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

        with section():
            refs["list"] = ui.column().classes("w-full gap-4")
            ui.element("div").style("height: 16px;")

    await reload()


def _render_levels(container: ui.column, challenges: list[dict]) -> None:
    """Agrupa por nivel y renderiza un mini-header por grupo + sus tarjetas."""
    container.clear()
    if not challenges:
        with container:
            with card():
                empty_state("emoji_events", "No challenges available yet")
        return

    by_level: dict[int, list[dict]] = {}
    for c in challenges:
        by_level.setdefault(c["level"], []).append(c)

    with container:
        for level in sorted(by_level.keys()):
            items = by_level[level]
            meta = LEVEL_META.get(level, {"name": f"Level {level}", "color": theme.SECONDARY, "icon": "star"})
            completed_in_level = sum(1 for c in items if c["completed"])
            level_locked = all(c["locked"] for c in items) and level > 1

            # Header del nivel
            with ui.row().classes("w-full items-center gap-2 no-wrap").style(
                "padding: 4px 4px;"
            ):
                with ui.element("div").style(
                    f"background: {meta['color']}1f; width: 32px; height: 32px; "
                    "border-radius: 10px; display: flex; align-items: center; "
                    "justify-content: center;"
                ):
                    ui.icon(meta["icon"]).style(
                        f"color: {meta['color']}; font-size: 18px;"
                    )
                with ui.column().classes("flex-1 gap-0"):
                    ui.label(meta["name"].upper()).style(
                        f"color: {meta['color']}; font-size: 11px; font-weight: 700; "
                        "letter-spacing: 1px;"
                    )
                    ui.label(f"{completed_in_level} / {len(items)} completed").style(
                        f"color: {theme.GREY_TEXT}; font-size: 11px;"
                    )
                if level_locked:
                    prev_name = LEVEL_META.get(level - 1, {}).get("name", "")
                    with ui.row().classes("items-center gap-1").style(
                        f"background: {theme.GREY_BG}; padding: 4px 10px; border-radius: 8px;"
                    ):
                        ui.icon("lock").style(
                            f"color: {theme.GREY_SOFT}; font-size: 14px;"
                        )
                        ui.label(
                            f"Finish {UNLOCK_THRESHOLD} of {prev_name}"
                        ).style(
                            f"color: {theme.GREY_SOFT}; font-size: 11px; font-weight: 600;"
                        )

            for c in items:
                _challenge_card(c)


def _challenge_card(challenge: dict) -> None:
    meta = KIND_META.get(challenge["kind"], {"icon": "emoji_events", "subtitle": ""})
    level_meta = LEVEL_META.get(
        challenge["level"], {"color": theme.SECONDARY, "name": "Challenge"}
    )
    color = level_meta["color"]
    completed = challenge.get("completed", False)
    locked = challenge.get("locked", False)
    best = challenge.get("best_xp", 0)
    target_path = f"/{challenge['kind']}/{challenge['challenge_id']}"

    cursor = "not-allowed" if locked else "pointer"
    opacity = "0.55" if locked else "1"

    row = ui.row().classes("w-full no-wrap items-stretch gap-0 fapp-card").style(
        f"padding: 0; overflow: hidden; cursor: {cursor}; opacity: {opacity};"
    )
    if not locked:
        row.on("click", lambda p=target_path: ui.navigate.to(p))

    with row:
        ui.element("div").style(f"width: 5px; background-color: {color};")
        with ui.row().classes("flex-1 no-wrap items-center gap-3").style("padding: 14px;"):
            with ui.element("div").style(
                f"background: {color}1f; width: 44px; height: 44px; border-radius: 12px; "
                "display: flex; align-items: center; justify-content: center; flex-shrink: 0;"
            ):
                ui.icon("lock" if locked else meta["icon"]).style(
                    f"color: {color}; font-size: 22px;"
                )
            with ui.column().classes("flex-1 gap-0").style("min-width: 0;"):
                with ui.row().classes("items-center gap-2 no-wrap"):
                    ui.label(challenge["title"]).classes("flex-1").style(
                        f"color: {theme.PRIMARY}; font-size: 15px; font-weight: 700; "
                        "white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"
                    )
                    if completed:
                        ui.label("DONE").style(
                            f"background-color: {theme.ACCENT}26; color: {theme.ACCENT}; "
                            "padding: 2px 8px; border-radius: 6px; font-size: 9.5px; "
                            "font-weight: 700; letter-spacing: 0.5px; flex-shrink: 0;"
                        )
                ui.label(meta["subtitle"]).style(
                    f"color: {theme.GREY_TEXT}; font-size: 12px;"
                )
                if locked:
                    ui.label("Locked").style(
                        f"color: {theme.GREY_SOFT}; font-size: 11px; font-weight: 600; "
                        "margin-top: 2px;"
                    )
                else:
                    ui.label(
                        f"Best: {best} XP" if completed else f"Earn up to {challenge['xp_reward']} XP"
                    ).style(
                        f"color: {color}; font-size: 11px; font-weight: 600; margin-top: 2px;"
                    )
            if not locked:
                ui.icon("chevron_right").style(
                    f"color: {theme.GREY_SOFT}; font-size: 22px; flex-shrink: 0;"
                )

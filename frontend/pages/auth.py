"""Login y Register. UC-01: Register Account."""

from datetime import date

from nicegui import ui

import api
import state
import theme
from layout import page_setup, primary_button


def _branded_header(title: str, subtitle: str) -> None:
    page_setup()
    with ui.element("div").classes("w-full").style(
        "background: linear-gradient(150deg, #0D1B3E 0%, #16213E 52%, #1e3574 100%); "
        "padding: 56px 28px 44px 28px;"
    ):
        with ui.column().classes("w-full max-w-[480px] mx-auto gap-0 items-start"):
            with ui.element("div").style(
                "width: 58px; height: 58px; border-radius: 16px; margin-bottom: 20px; "
                "background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.18); "
                "display: flex; align-items: center; justify-content: center;"
            ):
                ui.icon("savings").style("color: white; font-size: 30px;")
            ui.label("FAPP").style(
                "color: rgba(255,255,255,0.4); font-size: 10px; font-weight: 700; "
                "letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 10px;"
            )
            ui.label(title).style(
                "color: white; font-size: 28px; font-weight: 800; "
                "letter-spacing: -0.5px; line-height: 1.2;"
            )
            ui.label(subtitle).style(
                "color: rgba(255,255,255,0.5); font-size: 14px; margin-top: 6px;"
            )


def _form_container():
    return ui.column().classes("w-full max-w-[480px] mx-auto gap-4").style(
        f"background: {theme.WHITE}; padding: 28px 24px; "
        "min-height: calc(100vh - 270px);"
    )


@ui.page("/login")
def login_page():
    if state.is_authenticated():
        ui.navigate.to("/")
        return

    _branded_header("Welcome back", "Log in to your account")

    with _form_container():
        email = ui.input("Email").props("outlined rounded dense autofocus").classes("w-full")
        password = ui.input(
            "Password", password=True, password_toggle_button=True
        ).props("outlined rounded dense").classes("w-full")
        error_label = ui.label("").style(
            f"color: {theme.ERROR}; font-size: 13px; min-height: 18px;"
        )

        async def submit() -> None:
            if not email.value or not password.value:
                error_label.text = "Please fill in all fields"
                return
            error_label.text = ""
            btn.props("loading")
            try:
                data = await api.login(email.value.strip(), password.value)
                state.set_auth(data["token"], data["user_id"])
                ui.navigate.to("/")
            except api.ApiException as e:
                error_label.text = e.message
            finally:
                btn.props(remove="loading")

        # Enter submite el form desde cualquier campo
        email.on("keydown.enter", submit)
        password.on("keydown.enter", submit)

        btn = primary_button("Log in", submit)

        with ui.row().classes("w-full justify-center gap-1").style("margin-top: 12px;"):
            ui.label("Don't have an account?").style(
                f"color: {theme.GREY_TEXT}; font-size: 13px;"
            )
            ui.link("Create one", "/register").style(
                f"color: {theme.SECONDARY}; font-size: 13px; font-weight: 600;"
            )


@ui.page("/register")
def register_page():
    if state.is_authenticated():
        ui.navigate.to("/")
        return

    _branded_header("Create your account", "Start managing your finances today")

    with _form_container():
        with ui.row().classes("w-full gap-3 no-wrap"):
            name = ui.input("First name").props(
                "outlined rounded dense"
            ).classes("flex-1")
            surname = ui.input("Last name").props(
                "outlined rounded dense"
            ).classes("flex-1")

        birthdate = ui.input("Birthdate (YYYY-MM-DD)", value="2008-01-01").props(
            "outlined rounded dense readonly"
        ).classes("w-full")
        with birthdate.add_slot("append"):
            ui.icon("event").classes("cursor-pointer").on(
                "click", lambda: bd_dialog.open()
            )
        with ui.dialog() as bd_dialog, ui.card():
            ui.date(
                value="2008-01-01",
                on_change=lambda e: setattr(birthdate, "value", e.value),
            ).props("mask=YYYY-MM-DD")
            ui.button("OK", on_click=bd_dialog.close).props("flat")

        email = ui.input("Email").props("outlined rounded dense").classes("w-full")
        password = ui.input(
            "Password (min 6 chars)", password=True, password_toggle_button=True
        ).props("outlined rounded dense").classes("w-full")

        terms = ui.checkbox(
            "I accept the Terms of Service and Privacy Policy", value=False
        ).style(f"color: {theme.GREY_TEXT}; font-size: 13px;")
        error_label = ui.label("").style(
            f"color: {theme.ERROR}; font-size: 13px; min-height: 18px;"
        )

        async def submit() -> None:
            if not all([
                name.value, surname.value, email.value, password.value, birthdate.value
            ]):
                error_label.text = "Please fill in all fields"
                return
            if len(password.value) < 6:
                error_label.text = "Password must be at least 6 characters"
                return
            try:
                date.fromisoformat(birthdate.value)
            except ValueError:
                error_label.text = "Birthdate must be YYYY-MM-DD"
                return
            if not terms.value:
                error_label.text = "You must accept the terms"
                return
            error_label.text = ""
            btn.props("loading")
            try:
                data = await api.register(
                    name.value.strip(),
                    surname.value.strip(),
                    birthdate.value,
                    email.value.strip(),
                    password.value,
                )
                state.set_auth(data["token"], data["user_id"])
                ui.navigate.to("/")
            except api.ApiException as e:
                error_label.text = e.message
            finally:
                btn.props(remove="loading")

        btn = primary_button("Create account", submit)

        with ui.row().classes("w-full justify-center gap-1").style("margin-top: 12px;"):
            ui.label("Already have an account?").style(
                f"color: {theme.GREY_TEXT}; font-size: 13px;"
            )
            ui.link("Log in", "/login").style(
                f"color: {theme.SECONDARY}; font-size: 13px; font-weight: 600;"
            )

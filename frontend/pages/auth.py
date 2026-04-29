"""Login y Register. UC-01: Register Account."""

from datetime import date

from nicegui import ui

import api
import state
import theme
from layout import page_setup, primary_button


def _branded_header(title: str, subtitle: str) -> None:
    page_setup()
    with ui.column().classes("w-full max-w-[480px] mx-auto gap-0").style(
        f"background-color: {theme.WHITE}; padding: 32px 24px 0 24px;"
    ):
        with ui.column().classes("w-full items-center gap-2").style("margin-top: 24px;"):
            ui.icon("savings").style(f"color: {theme.SECONDARY}; font-size: 56px;")
            ui.label("FAPP").style(
                f"color: {theme.PRIMARY}; font-size: 28px; font-weight: 800; "
                "letter-spacing: -0.5px;"
            )
        with ui.column().classes("w-full items-center gap-1").style("margin-top: 24px;"):
            ui.label(title).style(
                f"color: {theme.PRIMARY}; font-size: 24px; font-weight: 700;"
            )
            ui.label(subtitle).style(f"color: {theme.GREY_TEXT}; font-size: 14px;")


def _form_container():
    return ui.column().classes("w-full max-w-[480px] mx-auto gap-3").style(
        f"background-color: {theme.WHITE}; padding: 24px; min-height: calc(100vh - 220px);"
    )


@ui.page("/login")
def login_page():
    if state.is_authenticated():
        ui.navigate.to("/")
        return

    _branded_header("Welcome back", "Sign in to continue")

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

        btn = primary_button("Sign in", submit)

        with ui.row().classes("w-full justify-center gap-1").style("margin-top: 12px;"):
            ui.label("Don't have an account?").style(
                f"color: {theme.GREY_TEXT}; font-size: 13px;"
            )
            ui.link("Register", "/register").style(
                f"color: {theme.SECONDARY}; font-size: 13px; font-weight: 600;"
            )


@ui.page("/register")
def register_page():
    if state.is_authenticated():
        ui.navigate.to("/")
        return

    _branded_header("Create your account", "Start your financial journey")

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
            "I agree to the Terms and Privacy Policy", value=False
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
            ui.link("Sign in", "/login").style(
                f"color: {theme.SECONDARY}; font-size: 13px; font-weight: 600;"
            )

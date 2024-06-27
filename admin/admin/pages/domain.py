"""The home page of the app."""

from admin.templates import template
from admin.system import load_env_dict, restart

import reflex as rx

BASE_DOMAIN = 'BASE_DOMAIN'


class DomainPageState(rx.State):
    form_data: dict[str, str] = load_env_dict()

    def restart(self, form_data: dict):
        self.form_data[BASE_DOMAIN] = form_data[BASE_DOMAIN]
        restart(self.form_data.copy())
        self.form_data = load_env_dict()


def dynamic_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.text(BASE_DOMAIN),
                rx.input(
                    name=BASE_DOMAIN,
                    placeholder=DomainPageState.form_data[BASE_DOMAIN]
                )
            ),
            rx.button("Restart", type="submit")
        ),
        on_submit=DomainPageState.restart
    )


@template(route="/", title="Domain")
def domain() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return rx.vstack(
        rx.heading("Domain settings", size='8'),
        dynamic_form()
    )

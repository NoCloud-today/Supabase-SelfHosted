"""The home page of the app."""

from admin import styles
from admin.templates import template
from admin.system import load_env_dict

import os
import reflex as rx
from dotenv import dotenv_values

BASE_DOMAIN = 'BASE_DOMAIN'

path_to_supabase_env = os.getenv('ENV_FILE_PATH')
config_dict = dotenv_values(dotenv_path=path_to_supabase_env)


class DomainPageState(rx.State):
    form_data: dict[str, str] = load_env_dict()

    def restart(self, form_data: dict):
        pass


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

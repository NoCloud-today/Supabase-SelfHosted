"""The dashboard page."""
import os.path

from admin.templates import template

import re
import reflex as rx
from dotenv import dotenv_values

path_to_supabase_env = os.getenv('ENV_FILE_PATH')
config_dict = dotenv_values(dotenv_path=path_to_supabase_env)
config_keys_array = [str(key) for key in config_dict.keys()]


class DynamicFormState(rx.State):
    form_data: dict = {}
    form_fields: list[str] = config_keys_array

    def handle_submit(self, form_data: dict):
        self.form_data = form_data

        with open(path_to_supabase_env, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            for key, value in self.form_data.items():
                if value != '':
                    if re.search(rf"{re.escape(key)}=(.*)", line):
                        lines[i] = f"{key}={value}\n"

        with open(path_to_supabase_env, 'w') as file:
            file.writelines(lines)

        print("File updated successfully.")


def display_config_value(config):
    return rx.hstack(
        rx.text(str(config)),
        rx.input(
            # placeholder=str(config[1]),
            name=str(config)
        )
    )


def dynamic_form():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.foreach(
                    DynamicFormState.form_fields,
                    lambda field, idx: rx.hstack(
                        rx.text(field),
                        rx.input(
                            name=field,
                        )
                    )
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=DynamicFormState.handle_submit,
            # reset_on_submit=True,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(DynamicFormState.form_data.to_string()),
    )


@template(route="/environment", title="Environment")
def environment() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Configuration parameters", size="8"),
        dynamic_form(),
        rx.button(
            "Restart Supabase",
            color_scheme="grass",
            # on_click=restart()
        )
    )
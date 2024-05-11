import json
from os import system
from typing import Any, Iterable
from rich.console import Console
from rich.theme import Theme

theme = Theme({
    "error": "bold red",
    "warning": "bold yellow",
    "success": "bold green",
})
console = Console(theme=theme)
print = console.print

# file paths
ADMIN_FILE_PATH = "Data/admin.json"
USERS_FILE_PATH = "Data/users.json"
EMAILS_FILE_PATH = "Data/emails.json"
PROJECTS_FILE_PATH = "Data/projects.json"
TITLES_FILE_PATH = "Data/titles.txt"


def clear_screen():
    system("cls||clear")


def get_bool_input(message: str, true: str, false: str, cls=True) -> bool:
    rep = 0
    while True:
        if cls:
            clear_screen()
        if rep > 0:
            print("Invalid input")
        choice = input(message)
        if choice in true:
            return True
        elif choice in false:
            return False
        rep += 1


def get_input(message: str, accepted_values: Iterable, cls=True, error_message="invalid input", return_type=str):
    accepted_values = [str(x) for x in accepted_values]

    error_sign = "$$error$$"
    if error_sign not in message:
        message = error_sign + "\n" + message

    is_valid = True
    while True:
        if cls:
            clear_screen()

        replacement = ""
        if not is_valid:
            replacement = "[red]" + error_message + "[/]"

        is_valid = True
        modified_message = message.replace(error_sign, replacement)
        print(modified_message, end="")
        choice = input()
        if choice not in accepted_values:
            is_valid = False
        if is_valid:
            return return_type(choice)


# Writes data into given json file:
def save_data(data: dict, saving_file: str) -> None:
    with open(saving_file, "w") as data_file:
        json.dump(data, data_file)


# Loads data from the given file:
def load_data(loading_file: str) -> Any:
    with open(loading_file, "r") as data_file:
        if loading_file.endswith(".json"):
            return json.load(data_file)
        else:
            return data_file.read()


# load_data but retruns empty dict in case of an error:
def handeled_load_data(loading_file: str) -> dict:
    try:
        return load_data(loading_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


TITLES_FILE_PATH = "Data/titles.txt"
TITLES = load_data(TITLES_FILE_PATH).split("\n\n")
TITLE = TITLES[5]
COLORED_TITLE = f"[cyan]{TITLE}[/]"

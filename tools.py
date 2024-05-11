import json
from os import system
from typing import Any
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
TITLES_FILE_PATH = "Data/titles.txt"


def get_bool_input(massage: str, true: str, false: str, cls=True) -> None:
    rep = 0
    while True:
        if cls:
            system("cls||clear")
        if rep > 0:
            print("Invalid input")
        choice = input(massage)
        if choice in true:
            return True
        elif choice in false:
            return False
        rep += 1


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


TITLES = load_data(TITLES_FILE_PATH).split("\n\n")
TITLE = TITLES[5]

import json
from os import system, path
from typing import Any, Iterable
from rich.console import Console
from rich.theme import Theme
from cryptography.fernet import Fernet

theme = Theme({
    "error": "bold red",
    "warning": "bold yellow",
    "success": "bold green",
})
console = Console(theme=theme)
print = console.print

# file paths
KEY_FILE_PATH = "Data/secret.key"
ADMIN_FILE_PATH = "Data/admin.json"
TASKS_FILE_PATH = "Data/tasks.json"
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
            console.print("Invalid input", style='error')
        console.print(message, style='warning')
        choice = input()
        if choice in true:
            return True
        elif choice in false:
            return False
        rep += 1


def get_input(message: str, included: Iterable = [], excluded: Iterable = [], cls=True, limiting_function=lambda x: True, error_message="invalid input", return_type=str):
    included = [str(x) for x in included]
    excluded = [str(x) for x in excluded]

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
        if included:
            if choice not in included:
                is_valid = False
        elif excluded:
            if choice in excluded:
                is_valid = False
        elif not limiting_function(choice):
            is_valid = False
        if is_valid:
            return return_type(choice)


# Writes data into given json file:
def save_data(data: Any, saving_file: str) -> None:
    with open(saving_file, "w") as data_file:
        if saving_file.endswith(".json"):
            json.dump(data, data_file, indent=2)
        else:
            data_file.write(data)


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
COLORED_TITLE = f"[cyan]{TITLE}[/]"


# helper class for defining classproperty
class ClassProperty:
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, owner):
        return self.fget.__get__(None, owner)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        self.fset.__get__(None, type(obj))(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    """
    decorator for defining class properties since class properties is deprecated in python 3.11
    and it's not possible to use both @property and @classmethod for a class method
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassProperty(func)


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def jsonized(obj):
    if type(obj) in [int, str]:
        return obj
    if type(obj) in [list, set]:
        return [jsonized(x) for x in obj]
    if hasattr(obj, "dump"):
        return obj.dump()
    return obj


def load_key():
    encryption_key = None
    if path.exists(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, "rb") as file:
            encryption_key = file.read()
    else:
        encryption_key = Fernet.generate_key()
        with open(KEY_FILE_PATH, "wb") as file:
            file.write(encryption_key)
    return encryption_key


encryption_key = load_key()


def encrypted(plain_text: str):
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.encrypt(plain_text.encode()).decode()


def decrypted(encrypted_text: str):
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(encrypted_text.encode()).decode()

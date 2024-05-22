from datetime import datetime
import json
from os import system, path
from typing import Any, Iterable
from rich.console import Console
from rich.theme import Theme
from rich import box
from rich.text import Text
from rich.table import Table
from cryptography.fernet import Fernet
from getpass import getpass
import re
from loguru import logger

log_format = "{time:YYYY-MM-DD HH:mm:ss}|{level}  |{extra[user]}  |{message}"
logger.configure(
    handlers=[{"sink": 'user-activity.log', "format": log_format}])


def log_user_activity(user, level, message):
    bound_logger = logger.bind(user=user)
    bound_logger.log(level, message)


theme = Theme({
    "error": "bold red",
    "warning": "bold yellow",
    "success": "italic green",
    "title": "black on cyan"
})
console = Console(theme=theme)
print = console.print

TIME_FORMAT = "%Y-%m-%d %H:%M"

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


def get_input(message: str, included: Iterable = [], excluded: Iterable = [], cls=True, limiting_function=lambda x: True,
              error_message="invalid input", return_type=str, is_pass=False, operation=None):
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
        if operation:
            operation()
        print(modified_message, end="")
        choice = None
        if is_pass:
            choice = getpass("")
        else:
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


# Writes data into given file:
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


def is_iterable(obj) -> bool:
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


def encrypted(plain_text: str) -> str:
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.encrypt(plain_text.encode()).decode()


def decrypted(encrypted_text: str) -> str:
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(encrypted_text.encode()).decode()


def pass_is_valid(password: str) -> bool:
    if len(password) < 6:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    if " " in password:
        return False
    return True


def email_is_valid(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False


def id_is_valid(id: str) -> bool:
    return id and " " not in id and "\t" not in id


def date_time_is_valid(date_time: str) -> bool:
    try:
        datetime.strptime(date_time, TIME_FORMAT)
    except:
        return False
    else:
        return True


def merged_tables(*args: Table) -> Table:
    table = Table(show_header=False, show_edge=False,
                  box=box.HORIZONTALS,)
    for _ in range(len(args)):
        table.add_column()
    table.add_row(*args)
    return table

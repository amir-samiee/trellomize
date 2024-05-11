import json
from os import system

admin_file_address = "Data/admin.json"
users_file_address = "Data/users.json"
emails_file_address = "Data/emails.json"


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
def save_data(data: dict, saving_file: str):
    with open(saving_file, "w") as data_file:
        json.dump(data, data_file)


# Loads data from the given json file:
def load_data(loading_file: str):
    with open(loading_file, "r") as data_file:
        return json.load(data_file)


# load_data but retruns empty dict in case of an error:
def handeled_load_data(loading_file: str):
    try:
        return load_data(loading_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

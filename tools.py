import json
from os import system


def get_bool_input(massage: str, cls=True) -> None:
    rep = 0
    while True:
        if cls:
            system("cls||clear")
        if rep > 0:
            print("Invalid input")
        choice = input(massage)
        if choice:
            if choice in "yY":
                return True
            elif choice in "nN":
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
        load_data(loading_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

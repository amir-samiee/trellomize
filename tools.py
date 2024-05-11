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
def save_data(self, data: dict, saving_file: str) -> None:
    with open(saving_file, "w") as data_file:
        json.dump(data, data_file)


# Loads data from the given json file:
def load_data(self, loading_file: str) -> dict:
    try:
        with open(loading_file, "r") as data_file:
            return json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

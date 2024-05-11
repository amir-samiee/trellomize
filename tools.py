import json
def get_bool_input(massage: str):
    rep = 0
    while True:
        if rep > 0:
            print("Invalid input")
        choice = input(massage)
        if choice in "yY":
            return True
        elif choice in "nN":
            return False
        rep += 1

# Writes data into given json file:
def save_data(self, data: dict, saving_file: str):
    with open(saving_file, "w") as data_file:
        json.dump(data, data_file)

        
# Loads data from the given json file:
def load_data(self, loading_file: str):
    try:
        with open(loading_file, "r") as data_file:
            return json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


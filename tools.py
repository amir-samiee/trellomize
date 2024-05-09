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

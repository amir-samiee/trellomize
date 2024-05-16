from tools import *
from base import *


class Menu:
    @staticmethod
    def login():
        clear_screen()
        message = f"{
            COLORED_TITLE}\n\n[italic green]Login:[/]\n$$error$$\nenter your username (0 to go back): "
        username = get_input(message, [*User.instances.keys(
        ), "0"], error_message="Username not found! You have to signup first")
        if username == "0":
            return
        user = User(username)
        if not user.is_active:
            # print(message)
            # print("Your account has been deactivated by the system admin! Press enter to go bacck to the first page: ", style="error")
            message += username + \
                "\n[error]Your account has been deactivated by the system admin!\nPress enter to go bacck to the first page: [/]"
            get_input(message)
            # input()
            return
        message += username + "\nenter your password (0 to go back): "
        password = get_input(
            message, included=[decrypted(user.password), "0"], error_message="wrong password", is_pass=True)
        if password == "0":
            return
        User.current = User(username)

    @staticmethod
    def signup():
        clear_screen()

        # getting name
        message = f"{
            COLORED_TITLE}\n\n[italic green]Signup:[/]\n$$error$$\nenter your name (0 to go back): "
        name = get_input(message)
        if name == "0":
            return

        # getting username
        message += name + "\nenter your username (0 to go back): "
        username = get_input(
            message, limiting_function=lambda x: x and x not in User.instances.keys(
            ) and " " not in x and "\t" not in x,
            error_message="Invalid username! Username already exists, includes whitespaces or is empty")
        if username == "0":
            return

        # getting email
        message += username + "\nenter your email (0 to go back): "
        email = get_input(message, limiting_function=lambda x: x == "0" or email_is_valid(
            x) and x not in [x["email"] for x in User.instances.values()], error_message="email is invalid or already in use")
        if email == "0":
            return

        # getting password
        message += email + "\nenter your password (0 to go back): "
        password = get_input(
            message, limiting_function=lambda x: x == "0" or pass_is_valid(x),
            error_message="password should be at least 6 characters including letters, digits and symbols (!@#$%...) and not any whitespaces`", is_pass=True)
        if password == "0":
            return

        # checking password
        message += "\nenter your password again (0 to go back): "
        repeated_password = get_input(
            message, [password, "0"], error_message="password doesn't match! try again", is_pass=True)
        if repeated_password == "0":
            return

        password = encrypted(password)
        user = User(username, password=password, name=name, email=email)
        save()
        User.current = user
        print("you successfully signed up! press enter to continue: ",
              style="success")
        input()

    @staticmethod
    def main():
        pass

    @staticmethod
    def starting():
        while True:
            clear_screen()
            options = f"{
                COLORED_TITLE}\n\n1. Login\n2. Signup\n0. Exit\n$$error$$\nenter your choice: "
            choice = get_input(options, range(3), return_type=int)
            match(choice):
                case 1:
                    Menu.login()
                case 2:
                    Menu.signup()
                case 0:
                    save()
                    quit()
            Menu.main()

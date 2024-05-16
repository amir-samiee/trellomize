"""
login
    menu:
        projects:
            new project
            my projects:
                leading (involved + ...)
                    *projects
                        add member
                        remove member
                        add task
                        info
                            change
                        delete project
                        *tasks (brief)
                            add member
                            remove member
                            delete task
                involved
                    *projects
                        info
                        *tasks (brief)
                            (change info)
                            add comment
        edit profile
        logout
        exit
"""
from tools import *
from base import *


def login():
    clear_screen()
    message = f"{
        COLORED_TITLE}\n\n[italic green]Login:[/]\n$$error$$\nenter your username (0 to go back): "
    username = get_input(message, [*User.instances.keys(
    ), "0"], error_message="Username not found! You have to signup first")
    if username == "0":
        return
    user = User(username)
    message += username + "\nenter your password (0 to go back): "
    password = get_input(
        message, included=[decrypted(user.password), "0"], error_message="wrong password", is_pass=True)
    if password == "0":
        return
    User.current = User(username)


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


def main_menu():
    pass


def starting_menu():
    while True:
        clear_screen()
        options = f"{
            COLORED_TITLE}\n\n1. Login\n2. Signup\n0. Exit\n$$error$$\nenter your choice: "
        choice = get_input(options, range(3), return_type=int)
        match(choice):
            case 1:
                login()
            case 2:
                signup()
            case 0:
                save()
                quit()
        main_menu()


if __name__ == "__main__":
    try:
        init_program()
        starting_menu()
    except KeyboardInterrupt:
        print("Exiting the program...", style="warning")
        save()

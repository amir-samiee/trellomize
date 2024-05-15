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
        COLORED_TITLE}\n\n$$error$$\nenter your username (0 to go back): "
    username = get_input(message, [*User.instances.keys(
    ), "0"], error_message="Username not found! You have to signup first")
    if username == "0":
        return
    user = User(username)
    message += username + "\nenter your password (0 to go back): "
    password = get_input(
        message, included=[decrypted(user.password), "0"], error_message="wrong password")
    if password == "0":
        return
    User.current = User(username)


def signup():
    pass


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

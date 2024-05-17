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
        Menu.main()

    @staticmethod
    def signup():
        clear_screen()

        # getting name
        message = f"{
            COLORED_TITLE}\n\n[italic green]Signup:[/]\n$$error$$\nenter your name (0 to go back): "
        name = get_input(message, limiting_function=lambda x: len(
            x) > 0, error_message="empty string not accepted")
        if name == "0":
            return

        # getting username
        message += name + "\nenter your username (0 to go back): "
        username = get_input(
            message, limiting_function=lambda x: x and x not in User.instances.keys(
            ) and id_is_valid(x),
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
        user = User(username, name, email, password)
        save()
        User.current = user
        print("you successfully signed up! press enter to continue: ",
              style="success")
        input()
        Menu.main()

    @staticmethod
    def new_project():
        clear_screen()

        options = "[title]NEW PROJECT[/]\n$$error$$\n(enter 0 to go back anytime)\nenter project's title: "
        title = get_input(options, limiting_function=lambda x: len(
            x) > 0, error_message="empty string not accepted")
        if title == "0":
            return

        options += title + "\nenter an id: "
        id = get_input(options, limiting_function=lambda x: x not in Project.instances.keys(
        ) and id_is_valid(x), error_message="id already exists or contains whitespaces")
        if id == "0":
            return

        options += id + "\nenter usernames to add to project, seperated by spaces: "
        members = set(get_input(options).split()) - {User.current.username}
        project = Project(id, title, User.current)
        for username in members:
            member = None
            try:
                member = User(username)
            except ValueError:
                print(f"Unable to add [cyan]{
                      username}[/]: [error]user doesn't exist[/]")
            else:
                project.add_member(member)
                print(f"{username} successfully added!", style="success")
        save()
        print("Project save!", style="success")
        input("press enter to go to the project: ")
        Menu.display_project(project, True)

    @staticmethod
    def display_project(project: Project, leading: bool):
        clear_screen()
        tasks_table = project.tasks_table()
        info_table = project.info_table()
        table = merge_tables(tasks_table, info_table)
        print(table)
        input()

    @staticmethod
    def display_projects(projects: list, leading: bool):
        while True:
            clear_screen()
            options = f"[title]{
                ["Involved", "Leading"][leading]} Projects[/]\n"
            for i in range(len(projects)):
                options += "\n" + str(i + 1) + ". " + projects[i].id
            options += "\n0. Back\n$$error$$\nenter your choice "
            choice = get_input(options, range(len(projects) + 1))
            if choice == "0":
                return
            Menu.display_project(projects[i], leading)

    @staticmethod
    def projects():
        options = f"{
            COLORED_TITLE}\n\n$$error$$\n1. New Project\n2. Involved Projects\n3. Leading Projects\n0. Back\n\nenter your choice: "
        while True:
            choice = get_input(options, range(4), return_type=int)
            match(choice):
                case 1:
                    Menu.new_project()
                case 2:
                    Menu.display_projects(list(User.current.involved), False)
                case 3:
                    Menu.display_projects(list(User.current.leading), True)
                case 0:
                    return

    @staticmethod
    def edit_profile():
        pass

    @staticmethod
    def main():
        options = f"{
            COLORED_TITLE}\n\n$$error$$\n1. Projects\n2. Edit Profile\n3. Logout\n0. Exit\n\nenter your choice: "
        while True:
            choice = get_input(options, range(4), return_type=int)
            match(choice):
                case 1:
                    Menu.projects()
                case 2:
                    Menu.edit_profile()
                case 3:
                    User.current = None
                    return
                case 0:
                    save_quit()

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

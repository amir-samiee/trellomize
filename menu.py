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
        logger.success(f"User '{user.username}' Logged in")
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
        logger.success(f"User '{user.username}' Signed up")
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
        project = Project(id, title, User.current)
        logger.success(
            f"User '{User.current.username}' Created project '{project.id}'")

        options += id + "\nenter usernames to add to project, seperated by spaces: "
        members = set(get_input(options).split()) - {User.current.username}
        for username in members:
            member = None
            try:
                member = User(username)
            except ValueError as err:
                logger.error(f"Unable to add '{
                             username}'.({err})")
                print(f"Unable to add [cyan]{
                      username}[/]: [error]user doesn't exist[/]")
            else:
                project.add_member(member)
                logger.success(f"User '{User.current.username}' Added user '{
                               member.username}' to project '{project.id}'")
                print(f"{username} successfully added!", style="success")
        save()
        print("Project saved!", style="success")
        input("press enter to go to the project: ")
        Menu.display_project(project, True)

    @staticmethod
    def display_task(project: Project, task: Task, leading: bool):
        while True:
            clear_screen()

            def op():
                print("Task\n", style="title")
                print(task.info_table())
            choice = None
            if leading:
                choice = get_input("enter your choice: ",
                                   range(11), operation=op, return_type=int)
            else:
                choice = get_input("enter your choice: ", [
                    8, 9, 0], error_message="you can only choose between items 8, 9 and 0 as a non-member of this task!", operation=op, return_type=int)
            match choice:
                case 1:
                    task_name = input("enter new name: ")
                    task.name = task_name
                    logger.success(f"User '{User.current.username}' updated task '{
                                   task.id}''s name to '{task.name}'")
                case 2:
                    print(
                        "enter a description for your task (enter twice to finish the description): ")
                    description = str()
                    while description[-2:] != "\n\n":
                        description += input() + "\n"
                    description = description[:-2]
                    task.description = description
                    logger.success(f"User '{User.current.username}' updated task '{
                                   task.id}''s description to '{task.description}'")
                case 3:
                    start_time = get_input(f"enter start time with this format <year>-<month>-<day> <hour>:<minute>\texample: {
                                           datetime.now().strftime(TIME_FORMAT)}\nor simply enter to set it to current: ",
                                           limiting_function=lambda x: date_time_is_valid(x) and datetime.strptime(
                                               x, TIME_FORMAT) <= task.end_time or x in ["", "0"], cls=False,
                                           error_message="invalid input! Note: input must follow the mentioned format and also be before the end time")
                    if start_time == "0":
                        continue
                    elif start_time == "":
                        start_time = datetime.now().strftime(TIME_FORMAT)
                    task.start_time = datetime.strptime(
                        start_time, TIME_FORMAT)
                    logger.success(f"User '{User.current.username}' updated task '{
                                   task.id}''s start_time to '{task.start_time}'")
                case 4:
                    end_time = get_input(f"enter end time with this format <year>-<month>-<day> <hour>:<minute>\t\texample: {
                        datetime.now().strftime(TIME_FORMAT)}\nor simply enter to set it to current: ",
                        limiting_function=lambda x: date_time_is_valid(x) and datetime.strptime(
                        x, TIME_FORMAT) >= task.start_time or x in ["", "0"], cls=False,
                        error_message="invalid input! Note: input must follow the mentioned format and also be after the start time")
                    if end_time == "0":
                        continue
                    elif end_time == "":
                        end_time = datetime.now().strftime(TIME_FORMAT)
                    task.end_time = datetime.strptime(
                        end_time, TIME_FORMAT)
                    logger.success(f"User '{User.current.username}' updated task '{
                                   task.id}''s end-time to '{task.end_time}'")
                case 5:
                    message = \
                        "use \"add <username 1> <username 2> ...\" to add a membeer\n" +\
                        "use \"remove <username 1> <username 2> ...\" to remove a member\n" +\
                        "enter 0 to cancel: "
                    choice = get_input(message, cls=False, limiting_function=lambda x: x == "0" or x.startswith(
                        "add") or x.startswith("remove"))
                    if choice == "0":
                        logger.info(f"Adding/Removing members to/from task '{task.id}' canceled")
                        continue
                    elif choice.startswith("add"):
                        usernames = choice[3:].split()
                        for username in usernames:
                            user = None
                            try:
                                user = User(username)
                            except ValueError as err:
                                print(f"undable to add {
                                      username}:[error] User doesn't exist")
                                logger.error(f"Unable to add User '{username}' to task '{task.id}'({err})")
                                continue

                            try:
                                task.add_member(user)
                            except Exception as err:
                                print(f"unable to add {
                                      username}:[error] {err}")
                                logger.error(f"Unable to add User '{username}' to task '{task.id}'({err})")
                                continue

                            print(f"{username} added successfully!",
                                  style="success")
                            logger.success(f"User '{User.current.username}' added user '{
                                           user.username}' to task '{task.id}'")
                        print("press enter to continue: ")
                        input()
                    elif choice.startswith("remove"):
                        usernames = choice[6:].split()
                        for username in usernames:
                            user = None
                            try:
                                user = User(username)
                            except ValueError as err:
                                print(f"undable to remove {
                                      username}:[error] User doesn't exist")
                                logger.error(f"Unable to remove User '{username}' from task '{task.id}'({err})")
                                continue

                            try:
                                task.remove_member(user)
                            except Exception as err:
                                print(f"unable to remove {
                                      username}:[error] {err}")
                                logger.error(f"Unable to remove User '{username}' from task '{task.id}'({err})")
                                continue

                            print(f"{username} removed successfully!",
                                  style="success")
                            logger.success(f"User '{User.current.username}' removed user '{
                                           user.username}' from task '{task.id}'")
                        print("press enter to continue: ")
                        input()
                case 6:
                    options = sorted(list(Priority), key=lambda x: x.value)
                    message = str()
                    for option in options:
                        message += str(option.value) + ". " + \
                            option.name + "\n"
                    message += "enter your choice: "
                    choice = get_input(message, range(
                        len(options)+1), return_type=int, cls=False)
                    if choice == 0:
                        continue
                    task.priority = options[choice-1]
                    logger.success(f"User '{User.current.username}' updated task '{
                                   task.id}''s priority to '{task.priority.name}'")
                case 7:
                    options = sorted(list(Status), key=lambda x: x.value)
                    message = str()
                    for option in options:
                        message += str(option.value) + ". " + \
                            option.name + "\n"
                    message += "enter your choice: "
                    choice = get_input(message, range(
                        len(options)+1), return_type=int, cls=False)
                    if choice == 0:
                        continue
                    task.status = options[choice-1]
                    logger.success(f"User '{User.current.username}' updated task '{
                                   task.id}''s status to '{task.status.name}'")
                case 8:
                    clear_screen()
                    print("History: ", task.name, style="title")
                    for comment in task.history:
                        print(comment)
                    print("press enter to continue: ", end="")
                    input()
                case 9:
                    while True:
                        clear_screen()
                        print("Comments: ", task.name, style="title")
                        for comment in task.comments:
                            print(comment.time.strftime(
                                TIME_FORMAT), style="dim", end=") ")
                            try:
                                print(f"[cyan]{comment.user.username}[/]: {
                                    comment.content}    ", end="")
                            except:
                                main_print(f"{color_dict["cyan"]}{comment.user.username}{
                                           color_dict["reset"]}: {comment.content}    ", end="")
                            print()
                        print("enter your comment (0 to go back): ", end="")
                        choice = input()
                        if not choice:
                            continue
                        if choice == "0":
                            break
                        comment = Comment(User.current, choice)
                        task.add_comment(Comment(User.current, choice))
                        logger.success(f"User '{User.current}' added a comment on task '{task.id}'")
                case 10:
                    print(
                        "are you [warning]SURE[/] you want to remove this task? (y/n): ", end="")
                    if input() == "y":
                        project.remove_task(task)
                        logger.success(
                            f"User '{User.current.username}' removed task '{task.id}'")
                        print(
                            "[success]task was successfully removed![/] press enter to continue: ", end="")
                        input()
                        return
                    logger.info(f"Removing task '{task.id}' canceled")
                    print(
                        "[warning]removing canceled! press enter to continue: ", end="")
                    input()
                case 0:
                    return

    @staticmethod
    def add_task(project: Project):
        task_name = input("enter task name: ")
        new_task = Task(task_name)
        project.add_task(new_task)
        logger.success(f"User '{User.current.username}' added task '{
                       new_task.id}' to project '{project.id}'")
        Menu.display_task(project, new_task, True)

    @staticmethod
    # returns if the user is still the leader of the project or not
    def edit_project(project: Project) -> bool:
        while True:
            def op():
                print(project.info_table_numbered())
            choice = get_input("enter your choice (0 to go back): ",
                               range(5), operation=op, return_type=int)
            match choice:
                case 1:
                    new_title = input("enter new title (0 to go back): ")
                    if new_title == "0":
                        continue
                    project.title = new_title
                    logger.success(f"User '{User.current.username}' updated project '{
                                   project.id}''s title to '{project.title}'")
                case 2:
                    new_id = get_input("enter new id: ", cls=False, excluded=Project.instances.keys(
                    ) | {""}, error_message="this id is currently in use or is empty")
                    logger.success(f"User '{User.current.username}' updated project '{
                                   project.id}''s id to '{new_id}'")
                    project.change_id(new_id)
                case 3:
                    new_leader = get_input("enter new leader's username: ", cls=False, included=project.members | {project.leader},
                                           error_message="user should already be a member of project")
                    project.leader = User(new_leader)
                    logger.success(f"User '{User.current.username}' changed project '{
                                   project.id}''s leader to '{project.leader.username}'")

                case 4:
                    message = \
                        "use \"add <username 1> <username 2> ...\" to add a membeer\n" +\
                        "use \"remove <username 1> <username 2> ...\" to remove a member\n" +\
                        "enter 0 to cancel: "
                    choice = get_input(message, cls=False, limiting_function=lambda x: x == "0" or x.startswith(
                        "add") or x.startswith("remove"))
                    adding = choice.startswith("add")
                    if choice == "0":
                        logger.info(f"Adding/Removing members to/from project '{project.id}' canceled")
                        continue
                    elif adding:
                        usernames = choice[3:].split()
                    elif not adding:
                        usernames = choice[6:].split()
                    for username in usernames:
                        user = None
                        try:
                            user = User(username)
                        except ValueError as err:
                            print(f"undable to {"add" if adding else "remove"} {
                                username}:[error] User doesn't exist")
                            logger.error(
                                f"Unable to{"add" if adding else "remove"} '{username}' {"to" if adding else "from"} project '{project.id}'.({err})")
                            continue
                        try:
                            project.add_member(
                                user) if adding else project.remove_member(user)
                        except Exception as err:
                            print(f"unable to {"add" if adding else "remove"} {
                                username}:[error] {err}")
                            logger.error(
                                f"unable to {"add" if adding else "remove"} '{username}' {"to" if adding else "from"} project '{project.id}'.({err})")
                            continue

                        print(f"{username} {"added" if adding else "removed"} successfully!",
                              style="success")
                        logger.success(f"User '{User.current.username}' {"added" if adding else "removed"} user '{
                            user.username}' {"to" if adding else "from"} project '{project.id}'")
                    print("press enter to continue: ")
                    input()
                case 0:
                    return project.leader == User.current

    @staticmethod
    def display_project(project: Project, leading: bool):
        while True:
            clear_screen()
            tasks_table = project.tasks_table()
            info_table = project.info_table()
            table = merged_tables(tasks_table, info_table)

            def op():
                print(table)
            included = [
                x.name + f" {y+1}" for x in Status for y in range(len(project.partitioned()[x]))] + ["0"]
            message = ""
            if leading:
                message += "1. Add Membeer  2. Remove Member    3. Add Task\n"
                message += "4. Edit Info    5. Remove Project   0. Back\n"
                included += [str(x) for x in range(1, 6)]
            else:
                message += "0. Back\n"
            message += "\nenter \"<status> <number>\" to specify a task"
            message += "\nenter your choice: "
            choice = get_input(message, limiting_function=lambda x: x.upper(
            ) in included, operation=op)
            message += choice + "\n"
            try:
                choice = int(choice)
            except:
                pass
            match choice:
                case 1:
                    included = {0} | User.instances.keys(
                    ) - {x.username for x in project.members} - {User.current.username}
                    choice = get_input(
                        message + "enter usernname (0 to cancel): ", included, operation=op)
                    if choice == "0":
                        logger.info(f"Adding member to project {project.id}' canceled")
                        continue
                    project.add_member(User(choice))
                    logger.success(f"User '{User.current.username}' added user '{
                        choice}' to project '{project.id}'")
                case 2:
                    choice = get_input(
                        message + "enter username (0 to cancel): ", {0} | {x.username for x in project.members}, operation=op)
                    if choice == "0":
                        logger.info(f"Removing member from project '{project.id}' canceled")
                        continue
                    project.remove_member(User(choice))
                    logger.success(f"User '{User.current.username}' removed user '{
                        choice}' from project '{project.id}'")
                case 3:
                    Menu.add_task(project)
                case 4:
                    if not Menu.edit_project(project):
                        leading = False
                case 5:
                    print(
                        "are you [warning]SURE[/] you want to remove this project? (y/n): ", end="")
                    if input() == "y":
                        project.remove()
                        logger.success(
                            f"User '{User.current.username}' removed project '{project.id}'")
                        return
                    logger.info(f"Removing project '{project.id}' canceled")
                    print(
                        "[warning]removing canceled! press enter to continue: ", end="")
                    input()
                case 0:
                    return
                case _:
                    st, index = choice.split()
                    st = STATUS_DICT[st.upper()]
                    index = int(index) - 1
                    task = project.partitioned()[st][index]
                    Menu.display_task(project,
                                      task, leading or task.has_member(User.current))

    @staticmethod
    def display_projects(leading: bool):
        projects = []
        while True:
            if leading:
                projects = User.current.leading
            else:
                projects = User.current.involved
            projects = list(projects)
            clear_screen()
            options = f"[title]{
                ["Involved", "Leading"][leading]} Projects[/]\n"
            for i in range(len(projects)):
                options += "\n" + str(i + 1) + ". " + projects[i].id
            options += "\n0. Back\n$$error$$\nenter your choice "
            choice = get_input(options, range(
                len(projects) + 1), return_type=int)
            if choice == 0:
                return
            Menu.display_project(projects[choice-1], leading)

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
                    Menu.display_projects(False)
                case 3:
                    Menu.display_projects(True)
                case 0:
                    return

    @staticmethod
    def edit_profile():
        user = User.current
        # user = User()
        while True:
            clear_screen()

            def op():
                print(user.info_table())
            choice = get_input("enter your choice: ", range(
                5), operation=op, return_type=int)
            match choice:
                case 1:
                    new_username = get_input(
                        "enter new username (0 to cancel): ", excluded=User.instances.keys(), cls=False)
                    if new_username == "0":
                        continue
                    user.change_username(new_username)
                case 2:
                    new_name = input("enter new name: ")
                    if new_name:
                        user.name = new_name
                case 3:
                    new_email = get_input("enter new email (0 to cancel): ", limiting_function=lambda x: x == "0" or email_is_valid(
                        x) and x not in [x["email"] for x in User.instances.values()], error_message="email is invalid or already in use", cls=False)
                    if new_email == "0":
                        continue
                    user.email = new_email
                case 4:
                    current_pass = get_input(
                        "enter your current password (0 to cancel): ", included=[decrypted(user.password), "0"], error_message="wrong password", is_pass=True, cls=False)
                    if current_pass == "0":
                        continue

                    new_pass = get_input(
                        "enter your new password (0 to cancel): ", limiting_function=lambda x: x == "0" or pass_is_valid(
                            x),
                        error_message="password should be at least 6 characters including letters, digits and symbols (!@#$%...) and not any whitespaces`", is_pass=True, cls=False)
                    if new_pass == "0":
                        continue

                    # checking password
                    repeated_pass = get_input(
                        "enter the new password again (0 to cancel): ", [new_pass, "0"], error_message="password doesn't match! try again", is_pass=True, cls=False)
                    if repeated_pass == "0":
                        continue
                    new_pass = encrypted(new_pass)
                    user.password = new_pass
                case 0:
                    return

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

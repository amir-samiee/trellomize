import argparse
from tools import *

console = console


class SystemManager:
    def __init__(self, admin_file=ADMIN_FILE_PATH,
                 users_file=USERS_FILE_PATH, projects_file=PROJECTS_FILE_PATH, tasks_file=TASKS_FILE_PATH) -> None:
        self.admin_data = admin_file
        self.users_data = users_file
        self.projects_data = projects_file
        self.tasks_data = tasks_file
        self.data = handeled_load_data(ADMIN_FILE_PATH)

    # Adds new admin if non exists:
    def create_admin(self, username: str, password: str) -> None:
        if bool(self.data):
            console.print("An admin already exists!", style='error')
            logger.error('Failed to create admin.(Admin already existed)')
            return
        if pass_is_valid(password):
            self.data[username] = encrypted(password)
            save_data(self.data, self.admin_file)
            console.print(
                f"Admin '{username}' saved successfully.", style='success')
            logger.success(f"Admin '{username}' has been created successfully")
        else:
            console.print(
                "password should be at least 6 characters including letters, digits and symbols (!@#$%...) and not any whitespaces`", style='error')
            logger.warning(f"Failed to create admin.(Bad password '{password}')")

    # Removes the existing admin:
    def remove_admin(self, username: str, password: str) -> None:
        if bool(self.data) and username in self.data.keys():
            if decrypted(self.data[username]) == (password):
                choice = get_bool_input(
                    f"Admin '{username}' would no longer exist\nProceed?(Y/N): ", "Yy", "Nn", False)
                if choice:
                    save_data({}, self.admin_file)
                    console.print(
                        f"Admin '{username}' deleted successfully.", style='success')
                    logger.success(f"admin '{username}' deleted successfully.")
                else:
                    console.print("Operation canceled", style='warning')
                    logger.info(f"Removing admin '{username}' canceled")
            else:
                console.print("Invalid Password", style='error')
                logger.warning(f"Removing admin '{username}' failed.(Invalid Password '{password}')")
        else:
            console.print("Admin does not exist!", style='error')
            logger.error(f"Removing admin '{username}' failed.(Admin '{username}' does not exist!)")

    # Deletes all existing data:
    def purge_data(self) -> None:
        if self.is_admin():
            choice = get_bool_input(
                "All data would be deleted\nProceed(Y/N): ", "Yy", "Nn", False
            )
            if choice:
                save_data({}, self.users_file)
                save_data({}, self.projects_file)
                save_data({}, self.tasks_file)
                console.print("Data purged successfully.", style='success')
                logger.success(f"Admin '{self.data.keys()[0]}' purged all data")
            else:
                console.print("Operation canceled", style='warning')
                logger.info("Purging data canceled")

    # Changing admin:
    def change(self, username: str, password: str) -> None:
        if self.is_admin():
            if pass_is_valid(password):
                save_data({username: encrypted(password)}, self.admin_file)
                console.print("Admin updated successfully!", style='success')
                logger.success(f"Admin updated successfully!('{username}' is the new admin)")
            else:
                console.print(
                    "password should be at least 6 characters including letters, digits and symbols (!@#$%...) and not any whitespaces`", style='error')
                logger.warning(f"Changing admin failed.(Bad password '{password}')")

    # Confirms if current user is the admin:
    def is_admin(self) -> bool:
        if bool(self.data):
            old_pass = ""
            for pas in self.data.values():
                old_pass = decrypted(pas)
            verify = getpass("Password: ")
            if verify != old_pass:
                console.print("Wrong password!", style='error')
                logger.warning(f"Admin authentication failed.(Wrong password '{verify}')")
                return False
            return True
        else:
            console.print("No admin exists", style='error')
            logger.error("Admin authentication failed.(No admin exists)")
            return False

    # Diactivates the given user:
    def ban(self, username: str):
        if self.is_admin():
            data = handeled_load_data(self.users_file)
            if username not in data.keys():
                console.print(
                    f"User '{username}' does not exist!", style='error')
                logger.error(f"Banning user failed.(user '{username}' does not exist)")
                return
            if data[username]['is_active'] == False:
                console.print(
                    f"User '{username}' is already banned!", style='error')
                logger.error(f"Banning user failed.(User '{username}' is already banned)")
                return
            data[username]['is_active'] = False
            save_data(data, self.users_file)
            console.print(f"User '{username}' banned", style='success')
            logger.success(f"Admin '{self.data.keys()[0]}' banned user '{username}'")

    # Activates users:
    def unban(self, username: str):
        if self.is_admin():
            data = handeled_load_data(self.users_file)
            if username not in data.keys():
                console.print(
                    f"User '{username}' does not exist!", style='error')
                logger.error(f"Unbanning failed.(User '{username}' does not exist)")
                return
            if data[username]['is_active'] == True:
                console.print(
                    f"User '{username}' is not banned!", style='error')
                logger.error(f"Unbanning failed.(User '{username}' is not banned)")
                return
            data[username]['is_active'] = True
            save_data(data, self.users_file)
            console.print(f"User '{username}' unbanned", style='success')
            logger.success(f"Admin '{self.data.keys()[0]}' unbanned user '{username}'")

    # Prints users:
    def view(self, substring='', banned_users=False):
        user_dict = handeled_load_data(self.users_file)
        i = 0
        if not banned_users:
            for username in user_dict.keys():
                if substring in username:
                    console.print(f"{i+1}- {username}")
        else:
            for username in user_dict.keys():
                if user_dict[username]['is_active'] == False:
                    console.print(f"{i+1}- {username}")

    # Creates a parser for managing system:
    def parser(self) -> argparse:
        # Creating the main parser:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(
            dest="subcommand", title="subcommands")

        # Create admin parser
        create_admin_parser = subparsers.add_parser(
            name="create-admin", help="Creates an admin"
        )
        create_admin_parser.add_argument(
            "-u", "--username", required=True, help="Admin's username"
        )
        create_admin_parser.add_argument(
            "-p", "--password", required=True, help="Admin's password"
        )

        # Admin parser:
        admin_parser = subparsers.add_parser(
            name="admin", help="Admin related tasks")
        admin_subparsers = admin_parser.add_subparsers(
            dest="admin_subcommand", title="admin_subcomands"
        )

        # Remove admin parser:
        remove_admin_parser = admin_subparsers.add_parser(
            name="remove", help="Removes admin"
        )
        remove_admin_parser.add_argument(
            "-u", "--username", required=True, help="Admin's username"
        )
        remove_admin_parser.add_argument(
            "-p", "--password", required=True, help="Admin's password"
        )

        # Change Admin info parser:
        change_info_parser = admin_subparsers.add_parser(
            name="change", help="Changes admin")
        change_info_parser.add_argument(
            "-u", "--username", required=True, help="Admin's new username"
        )
        change_info_parser.add_argument(
            "-p", "--password", required=True, help="Admin's new password"
        )

        # User parser:
        user_parser = subparsers.add_parser(
            name='user', help='User related tasks')
        user_subparsers = user_parser.add_subparsers(
            dest='user_subcommand', title='subcommands')

        # Ban user parser:
        ban_parser = user_subparsers.add_parser(name='ban', help='Ban users')
        ban_parser.add_argument(
            "-u", "--username", required=True, help="User's username"
        )

        # Unban user parser:
        unban_parser = user_subparsers.add_parser(
            name='unban', help='Unban users')
        unban_parser.add_argument(
            "-u", "--username", required=True, help="User's username"
        )

        # View users:
        view_parser = user_subparsers.add_parser(
            name='view', help='View users')
        view_group = view_parser.add_mutually_exclusive_group()
        view_group.add_argument(
            '-a', '--all', action='store_true', default=False, help='View all users')
        view_group.add_argument(
            '-s', '--search', help='View users with a certain substring')
        view_group.add_argument(
            '-b', '--banned', action='store_true', default=False, help='View banned users')

        # Purging data parser:
        purge_data_parser = subparsers.add_parser(
            name="purge-data", help="Deletes all data available"
        )

        return parser


if __name__ == "__main__":

    manager = SystemManager()

    parser = manager.parser()
    args = parser.parse_args()

    if args.subcommand == "create-admin":
        manager.create_admin(args.username, args.password)

    elif args.subcommand == "purge-data":
        manager.purge_data()

    elif args.subcommand == "admin":
        if args.admin_subcommand == "remove":
            manager.remove_admin(args.username, args.password)
        elif args.admin_subcommand == "change":
            manager.change(args.username, args.password)

    elif args.subcommand == "user":
        if args.user_subcommand == "view":
            if args.all:
                manager.view('')
            elif args.banned:
                manager.view(banned_users=True)
            else:
                manager.view(args.search)

        elif args.user_subcommand == "ban":
            manager.ban(args.username)
        elif args.user_subcommand == "unban":
            manager.unban(args.username)

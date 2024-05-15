import argparse
import tools

console = tools.console


class SystemManager:
    def __init__(self, admin_file=tools.ADMIN_FILE_PATH,
                 users_file=tools.USERS_FILE_PATH, emails_file=tools.EMAILS_FILE_PATH,
                 projects_file=tools.PROJECTS_FILE_PATH, ) -> None:
        self.admin_file = admin_file
        self.users_file = users_file
        self.emails_file = emails_file
        self.projects_file = projects_file

    # Adds new admin if non exists:
    def create_admin(self, username: str, password: str) -> None:
        data = dict(tools.handeled_load_data(self.admin_file))
        if bool(data):
            console.print("An admin already exists!", style='error')
        else:
            data[username] = password
            tools.save_data(data, self.admin_file)
            console.print(
                f"Admin '{username}' saved successfully.", style='success')

    # Removes the existing admin:
    def remove_admin(self, username: str, password: str) -> None:
        data = tools.handeled_load_data(self.admin_file)
        if bool(data) and username in data.keys():
            if data[username] == password:
                choice = tools.get_bool_input(
                    f"Admin '{username}' would no longer exist\nProceed?(Y/N): ", "Yy", "Nn", False)
                if choice:
                    tools.save_data({}, self.admin_file)
                    console.print(
                        f"admin '{username}' deleted successfully.", style='success')
                else:
                    console.print("Operation canceled", style='warning')
            else:
                console.print("Invalid Password", style='error')
        else:
            console.print("Admin does not exist!", style='error')

    # Deletes all existing data:
    def purge_data(self) -> None:
        if self.is_admin():
            choice = tools.get_bool_input(
                "All data would be deleted\nProceed(Y/N): ", "Yy", "Nn", False
            )
            if choice:
                tools.save_data({}, self.users_file)
                tools.save_data({}, self.emails_file)
                tools.save_data({}, self.projects_file)
                console.print("Data purged successfully.", style='success')
            else:
                console.print("Operation canceled", style='warning')

    # Changing admin:
    def change(self, username: str, password: str) -> None:
        if self.is_admin():
            tools.save_data({username: password}, self.admin_file)
            console.print("Admin updated successfully!", style='success')

    # Confirms if current user is the admin:
    def is_admin(self) -> bool:
        data = tools.handeled_load_data(self.admin_file)
        if bool(data):
            old_pass = ""
            for pas in data.values():
                old_pass = pas
            verify = input("Password: ")
            if verify != old_pass:
                console.print("Wrong password!", style='error')
                return False
            return True
        else:
            console.print("No admin exists", style='error')
            return False

    def ban(self, username: str):
        if self.is_admin():

            data = tools.handeled_load_data(self.users_file)
            if username not in data.keys():
                console.print(
                    f"User '{username}' does not exist!", style='error')
                return

            data[username]['is_active'] = False
            tools.save_data(data, self.users_file)
            console.print(f"User '{username}' banned", style='success')

    def view(self, substring=''):
        user_dict = tools.handeled_load_data(self.users_file)
        i = 1
        for username in user_dict.keys():
            if substring in username:
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

        # View users:
        view_parser = user_subparsers.add_parser(
            name='view', help='View users')
        view_group = view_parser.add_mutually_exclusive_group()
        view_group.add_argument(
            '-a', '--all', action='store_true', default=False, help='View all users')
        view_group.add_argument(
            '-s', '--search', help='View users with a certain substring')

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
            if not args.all:
                manager.view(args.search)
            else:
                manager.view('')
        elif args.user_subcommand == "ban":
            manager.ban(args.username)

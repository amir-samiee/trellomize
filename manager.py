import argparse
import tools


class SystemManager:

    def __init__(
        self,
        admin_file=tools.admin_file_address,
        users_file=tools.users_file_address,
        email_file=tools.emails_file_address,
    ):
        self.admin_file = admin_file
        self.users_file = users_file
        self.email_file = email_file

    # Adds new admin if non exists:
    def create_admin(self, username: str, password: str):
        data = dict(tools.handeled_load_data(self.admin_file))
        if bool(data):
            print("An admin already exists!")
        else:
            data[username] = password
            tools.save_data(data, self.admin_file)
            print(f"Admin '{username}' saved successfully.")

    # Removes the existing admin:
    def remove_admin(self, username: str, password: str):
        data = tools.handeled_load_data(self.admin_file)
        if bool(data) and username in data.keys():
            if data[username] == password:
                choice = tools.get_bool_input(
                    f"Admin '{username}' would no longer exist\nProceed?(Y/N): ",
                    "Yy",
                    "Nn",
                )
                if choice:
                    tools.save_data({}, self.admin_file)
                    print(f"admin '{username}' deleted successfully.")
                else:
                    print("Operation canceled")
            else:
                print("Invalid Password")
        else:
            print("Admin does not exist!")

    # Deletes all existing data:
    def purge_data(self):
        if self.is_admin():
            choice = tools.get_bool_input(
                "All data would be deleted\nProceed(Y/N): ", "Yy", "Nn"
            )
            if choice:
                tools.save_data({}, self.users_file)
                tools.save_data({}, self.email_file)
                print("Data purged successfully.")
            else:
                print("Operation canceled")

    # Changing admin:
    def change(self, username: str, password: str):
        if self.is_admin():
            tools.save_data({username: password}, self.admin_file)
            print("Admin updated successfully!")

    # Confirms if current user is the admin:
    def is_admin(self):
        data = tools.handeled_load_data(self.admin_file)
        if bool(data):
            old_pass = ""
            for pas in data.values():
                old_pass = pas
            verify = input("Password: ")
            if verify != old_pass:
                print("Wrong password!")
                return False
            return True
        else:
            print("No admin exists")
            return False

    # Creates a parser for managing system:
    def parser(self):
        # Creating the main parser:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(
            dest="subcommand", title="subcommands")

        # Creating admin parser
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
            name="change", help="Changes admin"
        )
        change_info_parser.add_argument(
            "-u", "--username", required=True, help="Admin's new username"
        )
        change_info_parser.add_argument(
            "-p", "--password", required=True, help="Admin's new password"
        )

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

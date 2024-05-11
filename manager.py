import argparse
import tools


class SystemManager:
    def __init__(self, admin_file="data/admin_data.json", database=""):
        self.admin_file = admin_file
        self.database = database

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
        if bool(data):
            if data[username] == password:
                choice = tools.get_bool_input(
                    f"admin '{username}' would no longer exist\nProceed?(y/n): ")
                if choice:
                    tools.save_data({}, self.admin_file)
                    print(f"admin '{username}' deleted successfully.")
                else:
                    print("Operation canceled")
            else:
                print("Invalid Password")
        else:
            print("No admin exists!")

    # Deletes all existing data:
    def purge_data(self):
        choice = tools.get_bool_input("All data would be deleted\nProceed(): ")
        if choice:
            tools.save_data({}, self.database)
            print("Data purged successfully.")
        else:
            print("Operation canceled")

    # Changing admin:
    def change(self, username: str, password: str):
        data = tools.handeled_load_data(self.admin_file)
        if bool(data):
            old_pass = ""
            for acc in data.values():
                old_pass = acc
            verify = input("Password: ")
            if verify != old_pass:
                print("Wrong password!")
                return

        tools.save_data({username: password}, self.admin_file)
        print("Admin's info updated successfully!")

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
        purge_data_parser.add_argument(
            "-p", "--password", required=True, help="Admin's password"
        )

        return parser


if __name__ == "__main__":

    manager = SystemManager()

    parser = manager.parser()
    args = parser.parse_args()

    if args.subcommand == "create-admin":
        manager.create_admin(args.username, args.password)

    elif args.subcommand == "purge-data":
        manager.purg_data()

    elif args.subcommand == "admin":
        if args.admin_subcommand == "remove":
            manager.remove_admin(args.username, args.password)
        elif args.admin_subcommand == "change":
            manager.change(args.username, args.password)

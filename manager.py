import json
import argparse
import tools

class Manager:

    def __init__(self, admin_file="admin_data.json", database=""):
        self.admin_file = admin_file
        self.database = database

    # Writes data into given json file:
    def save_data(self, data: dict, saving_file: str):
        with open(saving_file, "w") as data_file:
            json.dump(data, data_file)

    # Loads data from the given json file:
    def load_data(self, loading_file: str):
        try:
            with open(loading_file, "r") as data_file:
                return json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # Adds new admin if non exists:
    def create_admin(self, username: str, password: str):
        data = dict(self.load_data(self.admin_file))
        if bool(data):
            print("An admin already exists!")
        else:
            data[username] = password
            self.save_data(data, self.admin_file)
            print(f"Admin '{username}' saved successfully.")

    # Removes the existing admin:
    def remove_admin(self, username: str, password: str):
        data = self.load_data(self.admin_file)
        if bool(data):
            if data[username] == password:
                choice = tools.get_bool_input(
                    f"admin '{username}' would no longer exist\nProceed?(y/n): "
                )
                if choice:
                    self.save_data({}, self.admin_file)
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
            self.save_data({}, self.database)
            print("Data purged successfully.")
        else:
            print("Operation canceled")

    # Changing admin:
    def change_info(self, username: str, password: str):
        data = self.load_data(self.admin_file)
        if bool(data):
            old_pass = ""
            for acc in data.values():
                old_pass = acc
            verify = input("Password: ")
            if verify != old_pass:
                print("Wrong password!")
                return

        self.save_data({username: password}, self.admin_file)
        print("Admins info updated successfully!")

    def parser(self):
        # Creating the main parser:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="subcommand", title="subcommands")

        # Creating admin parser
        create_admin_parser = subparsers.add_parser(
            name="create-admin", help="Creates an admin"
        )
        create_admin_parser.add_argument(
            "-u", "--username", required=True, help="Admins username", metavar=""
        )
        create_admin_parser.add_argument(
            "-p", "--password", required=True, help="Admins password", metavar=""
        )

        # Admin parser:
        admin_parser = subparsers.add_parser(name="admin", help="Admin related tasks")
        admin_subparsers = admin_parser.add_subparsers(
            dest="admin_subcommand", title="admin_subcomands"
        )

        # Remove admin parser:
        remove_admin_parser = admin_subparsers.add_parser(
            name="remove", help="Removes admin"
        )
        remove_admin_parser.add_argument(
            "-u", "--username", required=True, help="Admins username", metavar=""
        )
        remove_admin_parser.add_argument(
            "-p", "--password", required=True, help="Admins password", metavar=""
        )

        # Change Admin info parser:
        change_info_parser = admin_subparsers.add_parser(
            name="change-info", help="Changes admin info"
        )
        change_info_parser.add_argument(
            "-u", "--username", required=True, help="Admins new username", metavar=""
        )
        change_info_parser.add_argument(
            "-p", "--password", required=True, help="Admins new password", metavar=""
        )

        # Purging data parser:
        purge_data_parser = subparsers.add_parser(
            name="purge-data", help="Deletes all data available"
        )
        purge_data_parser.add_argument(
            "-p", "--password", required=True, help="Admins password", metavar=""
        )

        return parser


if __name__ == "__main__":

    manager = Manager()

    parser = manager.parser()
    args = parser.parse_args()

    if args.subcommand == "create-admin":
        manager.create_admin(args.username, args.password)

    elif args.subcommand == "purge-data":
        manager.purg_data()

    elif args.subcommand == "admin":
        if args.admin_subcommand == "remove":
            manager.remove_admin(args.username, args.password)
        elif args.admin_subcommand == "change-info":
            manager.change_info(args.username, args.password)

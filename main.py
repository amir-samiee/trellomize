from menu import *


if __name__ == "__main__":
    try:
        init_program()
        Menu.starting()
    except ValueError as er:
        logger.exception(er)
    except KeyboardInterrupt:
        print("Exiting the program...", style="warning")
        save()

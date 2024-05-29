from menu import *


if __name__ == "__main__":
    try:
        init_program()
        Menu.starting()
    except ValueError as er:
        logger.exception(er)
        print("\nAn error occured!", style="error")
    except KeyboardInterrupt:
        print("\nExiting the program...", style="warning")
        save()

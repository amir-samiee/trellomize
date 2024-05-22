"""
login | signup | exit
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

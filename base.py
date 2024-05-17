import uuid
from datetime import datetime, timedelta
# from multipledispatch import dispatch
from enum import Enum
from tools import *


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


PRIORITY_DICT = {x.name: x for x in Priority}


class Status(Enum):
    BACKLOG = 1
    TODO = 2
    DOING = 3
    DONE = 4
    ARCHIVED = 5


STATUS_DICT = {x.name: x for x in Status}


class User:
    pass


class Task:
    pass


class Project:
    pass


class User:
    __current = None

    @classproperty
    def current(cls):
        current_user = User.__current
        if not current_user:
            raise ValueError("User has not been defined yet")
        return current_user

    @current.setter
    def current(cls, new_current_user):
        User.__current = new_current_user

    instances = dict()

    def __init__(self, username: str, name: str = '', email: str = '', password: str = None,
                 is_active: bool = True, involved=set(), leading=set()) -> None:
        if username not in User.instances:
            if password == None:
                raise ValueError("password can't be None")
            User.instances[username] = dict()
            self.username = username
            self.name = name
            self.email = email
            self.password = password
            self.is_active = is_active
            self.involved = involved
            self.leading = leading
        else:
            self.username = username

    def __eq__(self, other: User):
        return isinstance(other, User) and self.username == other.username

    def __hash__(self):
        return hash(self.username)

    def __repr__(self):
        return self.username

    def dump(self) -> dict:
        data = User.instances[self.username].copy()
        data["leading"] = [x.id for x in data["leading"]]
        data["involved"] = [x.id for x in data["involved"]]
        return data

    def __hash__(self):
        return hash(self.username)

    # @classmethod
    # def struct(cls, username: str, raw_dict: dict):
    #     data = {
    #         "name": "",
    #         "email": "",
    #         "password": None,
    #         "is_active": True,
    #         "involved": [],
    #         "leading": []
    #     }
    #     for key in data.keys():
    #         if key in raw_dict.keys():
    #             data[key] = raw_dict[key]
    #     User.instances[username] = data

    @classmethod
    def load_from_file(cls):
        User.instances = load_data(USERS_FILE_PATH)

    @classmethod
    def dump_to_file(cls):
        save_data(User.instances, USERS_FILE_PATH)

    @property
    def name(self):
        return User.instances[self.username]['name']

    @name.setter
    def name(self, new_name: str):
        User.instances[self.username]['name'] = new_name

    @property
    def email(self):
        return User.instances[self.username]['email']

    @email.setter
    def email(self, new_email: str):
        User.instances[self.username]['email'] = new_email

    @property
    def password(self):
        return User.instances[self.username]['password']

    @password.setter
    def password(self, new_password: str):
        User.instances[self.username]['password'] = new_password

    @property
    def is_active(self):
        return User.instances[self.username]['is_active']

    @is_active.setter
    def is_active(self, new_status: Status):
        User.instances[self.username]['is_active'] = new_status

    @property
    def leading(self):
        return set(Project(x) for x in User.instances[self.username]['leading'])

    @leading.setter
    def leading(self, new_leading: set):
        User.instances[self.username]['leading'] = [x.id for x in new_leading]

    @property
    def involved(self):
        return {Project(x) for x in User.instances[self.username]['involved']}

    @involved.setter
    def involved(self, new_involved: set):
        User.instances[self.username]['involved'] = [
            x.id for x in new_involved]

    @staticmethod
    def exists(user: (User | str)) -> bool:
        if type(user) == str:
            return user in User.instances.keys()
        elif type(user) == User:
            return user.username in User.instances.keys()
        raise ValueError(f'wrong type of argument({type(user)})')


# class Comment:
#     def __init__(self,user: User,) -> None:
#         pass


class Task:
    instances = dict()

    def __init__(self, name: str = "", description: str = "", start_time: datetime = datetime.now(),
                 end_time: datetime = datetime.now() + timedelta(days=1), members: set = set(), priority: Priority = Priority.LOW,
                 status: Status = Status.BACKLOG, history: list = [], comments: list = [], **kwargs) -> None:
        id = None
        if "id" in kwargs:
            id = kwargs["id"]
            self.id = id
            if id in Task.instances.keys():
                return
            raise ValueError("no task exists with this id")
        else:
            id = str(uuid.uuid4())
        self.id = id
        Task.instances[id] = dict()
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.members = members
        self.priority = priority
        self.status = status
        self.history = history
        self.comments = comments

    def __eq__(self, other: Task):
        return isinstance(other, Task) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    # @classmethod
    # def struct(cls, id, raw_dict):
    #     data = {
    #         "name": "",
    #         "description": "",
    #         "start_time": str(datetime.now()),
    #         "end_time":  str(datetime.now() + timedelta(days=1)),
    #         "members": [],
    #         "priority":  Priority.LOW.name,
    #         "status": Status.BACKLOG.name,
    #         "history": [],
    #         "comments": []
    #     }
    #     for key in data.keys():
    #         if key in raw_dict.keys():
    #             data[key] = raw_dict[key]
    #     Task.instances[id] = data

    @classmethod
    def load_from_file(cls):
        Task.instances = load_data(TASKS_FILE_PATH)

    @classmethod
    def dump_to_file(cls):
        save_data(Task.instances, TASKS_FILE_PATH)

    @property
    def name(self):
        return Task.instances[self.id]['name']

    @name.setter
    def name(self, new_name):
        Task.instances[self.id]['name'] = new_name

    @property
    def description(self):
        return Task.instances[self.id]['description']

    @description.setter
    def description(self, new_description):
        Task.instances[self.id]['description'] = new_description

    @property
    def start_time(self):
        return datetime.strptime(
            Task.instances[self.id]["start_time"], "%Y-%m-%d %H:%M:%S.%f")

    @start_time.setter
    def start_time(self, new_start_time):
        Task.instances[self.id]['start_time'] = str(new_start_time)

    @property
    def end_time(self):
        return datetime.strptime(
            Task.instances[self.id]["end_time"], "%Y-%m-%d %H:%M:%S.%f")

    @end_time.setter
    def end_time(self, new_end_time):
        Task.instances[self.id]['end_time'] = str(new_end_time)

    @property
    def members(self):
        return {User(x) for x in Task.instances[self.id]['members']}

    @members.setter
    def members(self, new_members):
        Task.instances[self.id]['members'] = [x.username for x in new_members]

    @property
    def priority(self):
        return PRIORITY_DICT[Task.instances[self.id]['priority']]

    @priority.setter
    def priority(self, new_priority: Priority):
        Task.instances[self.id]['priority'] = new_priority.name

    @property
    def status(self):
        return STATUS_DICT[Task.instances[self.id]['status']]

    @status.setter
    def status(self, new_status: Status):
        Task.instances[self.id]['status'] = new_status.name

    @property
    def history(self):
        return Task.instances[self.id]['history']

    @history.setter
    def history(self, new_history):
        Task.instances[self.id]['history'] = new_history

    @property
    def comments(self):
        return Task.instances[self.id]['comments']

    @comments.setter
    def comments(self, new_comments):
        Task.instances[self.id]['comments'] = new_comments

    @staticmethod
    def exists(task: (Task | str)) -> bool:
        if type(task) == str:
            return task in Task.instances.keys()
        elif type(task) == Task:
            return task.id in Task.instances.keys()
        raise ValueError(f'wrong type of argument({type(task)})')

    def has_member(self, user: User) -> bool:
        return user in self.members

    def add_member(self, user: User, is_viewed: bool = False) -> None:
        # Check if the user exists:
        if not User.exists(user):
            raise ValueError("User does not exist")
        task_members = self.members
        if user in task_members:
            raise ValueError(
                f"User '{user.username}' is already a member of the task")
        # Add user to the project:
        task_members.add(user)
        self.members = task_members
        if is_viewed:
            print(f"User '{user.username}' added to task '{
                  self.name}'", style='success')

    def remove_member(self, user: User, is_viewed: bool = False) -> None:
        # Check if the user exists:
        if not User.exists(user):
            raise ValueError(f"User does not exist")
        # Check if the user is a member of the task:
        if not self.has_member(user):
            raise ValueError(
                f"User '{user.username}' is not a part of the task")
        # Removing the user:
        members = self.members
        members.remove(user)
        self.members = members
        if is_viewed:
            print(f"User '{user.username}' removed from task '{
                  self.name}'", style='success')


class Project:
    instances = dict()

    def __init__(self, id: str, title: str = None, leader: User = None, members=set(), tasks=set()) -> None:
        self.id = id
        if id not in Project.instances.keys():
            if leader == None:
                raise ValueError(
                    "Invalid project ID or missing project title/leader.")
            # Creating and setting the data for instances
            Project.instances[id] = dict()
            self.title = title
            self.leader = leader
            self.members = members  # list of User instances
            self.tasks = tasks      # list of task identifiers or objects

            User.instances[leader.username]["leading"].append(id)
            for member in members:
                User.instances[member.username]["involved"].append(id)

    def __eq__(self, other: Project):
        return isinstance(other, Project) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    # @classmethod
    # def struct(cls, id, raw_dict):
    #     data = {
    #         "title": "",
    #         "leader": "",
    #         "members": [],
    #         "tasks": []
    #     }
    #     for key in data.keys():
    #         if key in raw_dict.keys():
    #             data[key] = raw_dict[key]
    #     Project.instances[id] = data

    @classmethod
    def load_from_file(cls):
        Project.instances = load_data(PROJECTS_FILE_PATH)

    @classmethod
    def dump_to_file(cls):
        save_data(Project.instances, PROJECTS_FILE_PATH)

    @property
    def title(self):
        return Project.instances[self.id]['title']

    @title.setter
    def title(self, new_title):
        Project.instances[self.id]['title'] = new_title

    @property
    def leader(self):
        return User(Project.instances[self.id]['leader'])

    @leader.setter
    def leader(self, new_leader: User):
        Project.instances[self.id]['leader'] = new_leader.username

    @property
    def members(self):
        return {User(x) for x in Project.instances[self.id]['members']}

    @members.setter
    def members(self, new_members):
        Project.instances[self.id]['members'] = [
            x.username for x in new_members]

    @property
    def tasks(self):
        return {Task(id=x) for x in Project.instances[self.id]['tasks']}

    @tasks.setter
    def tasks(self, new_tasks):
        Project.instances[self.id]['tasks'] = [x.id for x in new_tasks]

    def exists(project: (Project | str)) -> bool:
        if type(project) == str:
            return project in Project.instances.keys()
        elif type(project) == Project:
            return project.id in Project.instances.keys()
        raise ValueError(f'wrong type of argument({type(project)})')

    def has_member(self, user: User) -> bool:
        return user in self.members

    def is_leader(self, user: User) -> bool:
        return user == self.leader

    def task_belongs(self, task: Task) -> bool:
        return task in self.tasks

    def remove(self):
        # Remove project from leaders leading projects:
        self.leader.leading -= {self}

        # Remove project from members involved projects:
        for member in self.members:
            member.involved -= {self}

        # Remove tasks from task instances:
        for task in self.tasks:
            del Task.instances[task.id]

        # Remove project from project instances:
        del Project.instances[self.id]

    def add_member(self, user: User, is_viewed: bool = False) -> None:
        # Check if the user exists:
        if not User.exists(user):
            # console.print(f"User does not exist", style='error')
            raise ValueError("User does not exist")

        # Check if the user is not already in the project:
        if self.has_member(user) or self.is_leader(user):
            # console.print(f"User '{user.username}' is already a part of the project", style='error')
            raise ValueError(
                f"User '{user.username}' is already a part of the project")

        # Add user to the project:
        self.members |= {user}

        # Add project to the user:
        user.involved |= {self}

        if is_viewed:
            print(f"User '{user.username}' added to project",
                  f"'{self.title}'", style='success', sep=' ')

    def remove_member(self, user: User, is_viewed: bool = False) -> None:
        # Check if the user exists:
        if not User.exists(user):
            # console.print(f"User does not exist", style='error')
            raise ValueError(f"User does not exist")

        # Check if the user is the projects leader:
        if self.is_leader(user):
            # console.print('Cant remove the leader', style='error')
            raise ValueError('Cant remove the leader')

        # Check if the user is a member of project:
        if not self.has_member(user):
            # console.print(f"User '{user.username}' is not a part of the project", style='error')
            raise ValueError(
                f"User '{user.username}' is not a part of the project")

        # Removing the user:
        self.members -= {user}

        # Removing the user:
        user.involved -= {self}

        if is_viewed:
            console.print(f"User '{user.username}' removed from project",
                          f"'{self.title}'", style='success', sep=' ')

    def add_task(self, task: Task, is_viewed: bool = False):
        # Check if the task exists:
        if not Task.exists(task):
            # console.print(f"User does not exist", style='error')
            raise ValueError("task does not exist")

        # Check if the task is already in the project:
        if task.id in [t.id for t in self.tasks]:
            raise ValueError('Task already exists in the project')

        # Add task to the project:
        self.tasks |= {task}

        if is_viewed:
            print(f"Task '{task.name}' added to project",
                  f"'{self.title}'", style='success', sep=' ')

    def remove_task(self, task: Task, is_viewed: bool = False):
        # Check if the task exists:
        if not Task.exists(task):
            # console.print(f"User does not exist", style='error')
            raise ValueError("Task does not exist")

        # Check if the task is in  the project:
        if task.id not in [t.id for t in self.tasks]:
            raise ValueError('Task is not in the project')

        # Remove task from the project:
        self.tasks -= {task}

        if is_viewed:
            print(f"Task '{task.name}' removed from project",
                  f"'{self.title}'", style='success', sep=' ')

    def add_member_to_task(self, user: User, task: Task, is_viewed: bool = False) -> None:
        if not User.exists(user):
            # console.print(f"User does not exist", style='error')
            raise ValueError(f"User does not exist")

        # Check if the user is a part of the project:
        if not (self.has_member(user) or self.is_leader(user)):
            # console.print('User isnt a part of the project', style='error')
            raise ValueError('User isnt a part of the project')

        # Check if the task is valid:
        if not self.task_belongs(task):
            raise ValueError('The given task does not exist')

        task.add_member(user, is_viewed)

    def remove_member_from_task(self, user: User, task: Task, is_viewed: bool = False) -> None:
        if not User.exists(user):
            # console.print(f"User does not exist", style='error')
            raise ValueError(f"User does not exist")

        # Check if the task is valid:
        if not self.task_belongs(task):
            # console.print('The given task does not exist', style='error')
            raise ValueError('The given task does not exist')

        task.remove_member(user, is_viewed)


def init_program():
    User.load_from_file()
    Task.load_from_file()
    Project.load_from_file()


def save():
    User.dump_to_file()
    Task.dump_to_file()
    Project.dump_to_file()


def save_quit():
    save()
    quit()


def quit_check(choice: str, quit_sign="q"):
    if choice == quit_sign:
        save_quit()

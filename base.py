import uuid
from datetime import datetime, timedelta
from multipledispatch import dispatch
from enum import Enum


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class Status(Enum):
    BACKLOG = 1
    TODO = 2
    DOING = 3
    DONE = 4
    ARCHIVED = 5


class Task:
    pass


class Project:
    pass


class User:
    instances = dict()

    def __init__(self, username: str, name="", email="", password="",
                 is_active=True) -> None:
        self.username = username
        if username not in User.instances.keys():
            # Creating and setting the data for instances
            data = dict()
            data['name'] = name
            data['email'] = email
            data['password'] = password
            data['is_active'] = is_active
            data['leading'] = set()  # projects
            data['involved'] = set()  # projects
            User.instances[username] = data

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
        return User.instances[self.username]['leading']

    @leading.setter
    def leading(self, new_leading: list):
        User.instances[self.username]['leading'] = new_leading

    @property
    def involved(self):
        return User.instances[self.username]['involved']

    @involved.setter
    def involved(self, new_involved: list):
        User.instances[self.username]['involved'] = new_involved


# class Comment:
#     def __init__(self,user: User,) -> None:
#         pass


class Task:
    instances = dict()

    def __init__(self, name="", description="", start_time=datetime.now(),
                 end_time=datetime.now() + timedelta(days=1), members=set(), priority=Priority.LOW,
                 status=Status.BACKLOG, history=[], comments=[], **kwargs) -> None:
        id = None
        if "id" in kwargs:
            id = kwargs["id"]
        else:
            id = str(uuid.uuid4())
        self.id = id
        if id not in Task.instances.keys():
            data = dict()
            data["name"] = name
            data["description"] = description
            data["start_time"] = start_time
            data["end_time"] = end_time
            data["members"] = members
            data["priority"] = priority
            data["status"] = status
            data["history"] = history
            data["comments"] = comments
            Task.instances[self.id] = data

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
        return Task.instances[self.id]['start_time']

    @start_time.setter
    def start_time(self, new_start_time):
        Task.instances[self.id]['start_time'] = new_start_time

    @property
    def end_time(self):
        return Task.instances[self.id]['end_time']

    @end_time.setter
    def end_time(self, new_end_time):
        Task.instances[self.id]['end_time'] = new_end_time

    @property
    def members(self):
        return Task.instances[self.id]['members']

    @members.setter
    def members(self, new_members):
        Task.instances[self.id]['members'] = new_members

    @property
    def priority(self):
        return Task.instances[self.id]['priority']

    @priority.setter
    def priority(self, new_priority):
        Task.instances[self.id]['priority'] = new_priority

    @property
    def status(self):
        return Task.instances[self.id]['status']

    @status.setter
    def status(self, new_status):
        Task.instances[self.id]['status'] = new_status

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


class Project:
    instances = dict()

    def __init__(self, id: str, title="", leader=None, members=set(), tasks=set()) -> None:
        self.id = id
        if id not in Project.instances.keys():
            leader.leading.add(self)
            for member in members:
                member.involved.add(self)

            # Creating and setting the data for instances
            data = dict()
            data['title'] = title
            data['leader'] = leader
            data['members'] = members  # list of User instances
            data['tasks'] = tasks      # list of task identifiers or objects
            Project.instances[id] = data

    @property
    def title(self):
        return Project.instances[self.id]['title']

    @title.setter
    def title(self, new_title):
        Project.instances[self.id]['title'] = new_title

    @property
    def leader(self):
        return Project.instances[self.id]['leader']

    @leader.setter
    def leader(self, new_leader):
        Project.instances[self.id]['leader'] = new_leader

    @property
    def members(self):
        return Project.instances[self.id]['members']

    @members.setter
    def members(self, new_members):
        Project.instances[self.id]['members'] = new_members

    @property
    def tasks(self):
        return Project.instances[self.id]['tasks']

    @tasks.setter
    def tasks(self, new_tasks):
        Project.instances[self.id]['tasks'] = new_tasks

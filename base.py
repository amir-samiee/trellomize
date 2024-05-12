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


class User:
    instances = dict()

    def __init__(self, name: str, username: str, email: str, password: str,
                 is_active=True, leading_id=[], involved_id=[]) -> None:
        self.username = username

        # Creating and setting the data for instances
        data = dict()
        data['name'] = name
        data['email'] = email
        data['password'] = password
        data['is_active'] = is_active
        data['leading_id'] = leading_id  # projects
        data['involved_id'] = involved_id  # projects
        User.instances[username] = data

    @property
    def name(self):
        return User.instances[self.username]['name']

    @name.setter
    def name(self, new_name):
        User.instances[self.username]['name'] = new_name

    @property
    def email(self):
        return User.instances[self.username]['email']

    @email.setter
    def email(self, new_email):
        User.instances[self.username]['email'] = new_email

    @property
    def password(self):
        return User.instances[self.username]['password']

    @password.setter
    def password(self, new_password):
        User.instances[self.username]['password'] = new_password

    @property
    def is_active(self):
        return User.instances[self.username]['is_active']

    @is_active.setter
    def is_active(self, new_status):
        User.instances[self.username]['is_active'] = new_status

    @property
    def leading(self):
        return User.instances[self.username]['leading_id']

    @leading.setter
    def leading(self, new_leading):
        User.instances[self.username]['leading_id'] = new_leading

    @property
    def involved(self):
        return User.instances[self.username]['involved_id']

    @involved.setter
    def involved(self, new_involved):
        User.instances[self.username]['involved_id'] = new_involved


# class Comment:
#     def __init__(self,user: User,) -> None:
#         pass


class Task:
    instances = dict()

    def __init__(self, name: str, description="", id=uuid.uuid4(), start_time=datetime.now(),
                 end_time=datetime.now() + timedelta(days=1), members=[], priority=Priority.LOW,
                 status=Status.BACKLOG, history=[], comments=[],) -> None:
        self.id = id
        Task.instances = dict()

        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.members = members
        self.priority = priority
        self.status = status
        self.history = history
        self.comments = comments

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

    @dispatch(str, str, str, list, list)
    def __init__(self, title: str, id: str, leader: str, members=[], tasks=[]) -> None:
        self.id = id

        # Creating and setting the data for instances
        data = Project.instances[id] = dict()
        data['title'] = title
        data['leader'] = leader
        data['members'] = members  # list of User instances
        data['tasks'] = tasks      # list of task identifiers or objects
        Project.instances[id] = data

    @dispatch(str)
    def __init__(self, id: str):
        if id in Project.instances.keys:
            self.id = id
        else:
            raise KeyError("Project not defined yet")

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

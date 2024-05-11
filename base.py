import uuid
from datetime import datetime, timedelta
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
    def __init__(self, name: str, username: str, email: str, password: str,
                 is_active=True, leading=[], involved=[]) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.is_active = is_active
        self.leading = leading  # projects
        self.involved = involved  # projects


# class Comment:
#     def __init__(self,user: User,) -> None:
#         pass


class Task:
    def __init__(self, name: str, description="", id=uuid.uuid4(), start_time=datetime.now(),
                 end_time=datetime.now() + timedelta(days=1), members=[], priority=Priority.LOW,
                 status=Status.BACKLOG, history=[], comments=[],) -> None:
        self.name = name
        self.description = description
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.members = members
        self.priority = priority
        self.status = status
        self.history = history
        self.comments = comments


class Project:
    def __init__(self, title: str, id: str, leader: User, members=[], tasks=[]) -> None:
        self.title = title
        self.id = id
        self.leader = leader
        self.members = members
        self.tasks = tasks

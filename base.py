"""
login
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
    def __init__(self, name: str, email: str, password: str, is_active=True, leading=[], involved=[]) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.is_active = is_active
        self.leading = leading
        self.involved = involved

# class Comment:
#     def __init__(self,user: User,) -> None:
#         pass


class Task:
    def __init__(self, name: str, description="", id=uuid.uuid4(),
                 start_time=datetime.now(), end_time=datetime.now() + timedelta(days=1),
                 members=[], priority=Priority.LOW, status=Status.BACKLOG, history=[], comments=[]) -> None:
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
        self. members = members
        self.tasks = tasks

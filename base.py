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


priority_dict = {x.name: x for x in Priority}


class Status(Enum):
    BACKLOG = 1
    TODO = 2
    DOING = 3
    DONE = 4
    ARCHIVED = 5


status_dict = {x.name: x for x in Status}


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

    def cast(user):
        if not User.exists(user):
            return None
        elif type(user) == str:
            return User(user)
        elif type(user) == User:
            return user
        else:
            raise ValueError(f'wrong type argument({type(user)})')
        
    def dump(self) -> dict:
        data = User.instances[self.username].copy()
        # data["leading"] = [x.id for x in data["leading"]]
        # data["involved"] = [x.id for x in data["involved"]]
        return data

    def load(self, raw_dict: dict):
        data = raw_dict.copy()
        data["leading"] = set()
        data["involved"] = set()
        # data["leading"] = [Project(id=x) for x in data["leading"]]
        # data["involved"] = [Project(id=x) for x in data["involved"]]
        User.instances[self.username] = data

    @classmethod
    def load_from_file(cls):
        data = load_data(USERS_FILE_PATH)
        for username in data.keys():
            user_data = data[username]
            # user_data["leading"] = set()
            user = User(username)
            user.load(user_data)

    @classmethod
    def dump_to_file(cls):
        data = User.instances.copy()
        data = {x: User(x).dump() for x in data.keys()}
        with open(USERS_FILE_PATH, "w") as file:
            file.write(data)

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

    def exists(user):
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
    
    def cast(task):
        if not Task.exists(task):
            return None
        if type(task) == str:
            return Task(task)
        elif type(task) == Task:
            return task
        else:
            raise ValueError(f'wrong type argument({type(task)})')
        
    def dump(self):
        data = Task.instances[self.id].copy()
        data["start_time"] = str(data["start_time"])
        data["end_time"] = str(self.end_time)
        data["members"] = [x.dump() for x in self.members]
        data["priority"] = self.priority.name
        data["status"] = self.status.name
        return data

    def load(self, raw_dict: dict):
        data = raw_dict.copy()
        data["start_time"] = datetime.strptime(
            data["start_time"], "%Y-%m-%d %H:%M:%S.%f")
        data["end_time"] = datetime.strptime(
            data["end_time"], "%Y-%m-%d %H:%M:%S.%f")
        data["members"] = {User(username=x) for x in data["members"]}
        data["priority"] = priority_dict[data["priority"]]
        data["status"] = status_dict[data["status"]]
        Task.instances[self.id] = data

    @classmethod
    def load_from_file(cls):
        data = load_data(TASKS_FILE_PATH)
        for task_id in data.keys():
            task_data = data[task_id]
            task = Task(id=task_id)
            task.load(task_data)

    @classmethod
    def dump_to_file(cls):
        data = Task.instances.copy()
        data = {x: Task(id=x).dump() for x in data.keys()}
        with open(TASKS_FILE_PATH, "w") as file:
            file.write(data)

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

    def exists(self, task):
        if type(task) == str:
            return task in Task.instances.keys()        
        elif type(task) == Task:
            return task.id in Task.instances.keys()
        raise ValueError(f'wrong type of argument({type(task)})')
    
    
    def add_member(self, user):
        user = User.cast(user)        
        # Check if the user exists:
        if user == None:
            console.print(f"User does not exist", style='error')
            return
        
        task_members = self.members
        if user in task_members:
            console.print(f"User '{user.username}' is already a member of the task", style='error')
            return
        
        # Add user to the project:
        task_members.add(user)
        self.members = task_members

        console.print(f"User '{user.username}' added succesfully", style='success')


class Project:
    instances = dict()

    def __init__(self, id: str, title="", leader=None, members=set(), tasks=set()) -> None:
        self.id = id
        if id not in Project.instances.keys():
            if leader:
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

    def dump(self):
        data = Project.instances[self.id].copy()
        data["leader"] = self.leader.username
        data["members"] = [x.username for x in self.members]
        data["tasks"] = [x.id for x in self.tasks]
        return data

    def load(self, raw_dict: dict):
        data = raw_dict.copy()
        data["leader"] = User(data["leader"])
        data["members"] = {User(x) for x in data["members"]}
        data["tasks"] = {Task(id=x) for x in data["tasks"]}
        Project.instances[self.id] = data
        self.leader.leading.add(self)
        for member in self.members:
            member.involved.add(self)

    @classmethod
    def load_from_file(cls):
        data = load_data(PROJECTS_FILE_PATH)
        for project_id in data.keys():
            project_data = data[project_id]
            project = Project(id=project_id)
            project.load(project_data)

    @classmethod
    def dump_to_file(cls):
        data = Project.instances.copy()
        data = {x: Project(id=x).dump() for x in data.keys()}
        with open(PROJECTS_FILE_PATH, "w") as file:
            file.write(data)

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
    
    def is_member(self, user):
        user = User.cast(user)
        if user == None:
            print('User does not exist', style='error')
            return
        return user in self.members
    
    def is_leader(self, user):
        user = User.cast(user)
        if user == None:
            print('User does not exist', style='error')
            return
        return user == self.leader            

    def task_belongs(self, task):
        if type(task) == Task:
            return task in self.tasks
        elif type(task) == str:
            return task in [t.id for t in self.tasks]
        raise ValueError(f'wrong type argument({type(task)})')
    
    def add_member(self, user):
        user = User.cast(user)        
        # Check if the user exists:
        if user == None:
            console.print(f"User does not exist", style='error')
            return

        # Check if the user is not already in the project:
        if self.is_member(user) or self.is_leader(user):
            console.print(f"User '{user.username}' is already a part of the project", style='error')
            return
        
        # Add user to the project:
        members = self.members
        members.add(user)
        self.members = members

        console.print(f"User '{user.username}' added succesfully", style='success')

    
    def remove_member(self, user):
        
        user = User.cast(user)        
        # Check if the user exists:
        if user == None:
            console.print(f"User does not exist", style='error')
            return

        # Check if the user is the projects leader:
        if self.is_leader(user):
            console.print('Cant remove the leader', style='error')
            return
        
        # Check if the user is a member of project:
        if not self.is_member(user):
            console.print(f"User '{user.username}' is not a part of the project", style='error')
            return
        
        # Removing the user:
        members = self.members
        members.remove(user)
        self.members = members
        console.print(f"User '{user.username}' removed from the project succesfully", style='success')
    
    def add_member_to_task(self, user, task):
        
        # Check if the user is a part of the project:
        if not(self.is_member(user) or self.is_leader(user)):
            console.print('User isnt a part of the project', style='error')
            return
        
        # Check if the task is valid:
        if not self.task_belongs(task):
            console.print('The given task does not exist', style='error')
            return
        
        task = Task.cast(task)
        task.add_member(user)
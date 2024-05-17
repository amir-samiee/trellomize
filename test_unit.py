import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import uuid
from base import *

sample_tasks = {
    "1": {
        "name": "Task 1",
        "description": "Description 1",
        "start_time": str(datetime.now()),
        "end_time": str(datetime.now() + timedelta(days=1)),
        "members": [],
        "priority": "LOW",
        "status": "BACKLOG",
        "history": [],
        "comments": []
    },
    "2": {
        "name": "Task 2",
        "description": "Description 2",
        "start_time": str(datetime.now()),
        "end_time": str(datetime.now() + timedelta(days=2)),
        "members": [],
        "priority": "HIGH",
        "status": "TODO",
        "history": [],
        "comments": []
    }
}


@pytest.fixture
def clear_task_instances():
    """Fixture to clear Task.instances before and after each test"""
    Task.instances.clear()
    yield
    Task.instances.clear()


@pytest.fixture
def empty_task():
    return Task(name="Task Name", description="Task Description")


@pytest.fixture
def task_with_members():
    user1 = User(username="user1", name="User One",
                 email="user1@example.com", password="password")
    user2 = User(username="user2", name="User Two",
                 email="user2@example.com", password="password")
    return Task(name="New Task", description="New Description", priority=Priority.MEDIUM, status=Status.TODO, members={user1, user2})


@pytest.fixture
def user1():
    return User(username="user1", name="User One",
                email="user1@example.com", password="password")


@pytest.fixture
def user2():
    return User(username="user2", name="User Two",
                email="user2@example.com", password="password")


@pytest.fixture
def user3():
    return User(username="user3", name="User Three",
                email="user3@example.com", password="password")


def test_task_initialization_with_parameters(clear_task_instances, task_with_members, user1, user2):
    task = task_with_members
    assert task.id in Task.instances
    assert Task.instances[task.id]['name'] == "New Task"
    assert Task.instances[task.id]['description'] == "New Description"
    assert Task.instances[task.id]['priority'] == "MEDIUM"
    assert Task.instances[task.id]['status'] == "TODO"
    assert user1.username in Task.instances[task.id]['members']
    assert user2.username in Task.instances[task.id]['members']
    assert Task.instances[task.id]['history'] == []
    assert Task.instances[task.id]['comments'] == []
    assert isinstance(task.start_time, datetime)
    assert isinstance(task.end_time, datetime)


def test_task_reintialization_with_id(clear_task_instances, task_with_members):
    reloaded_task = Task(id=task_with_members.id)
    assert task_with_members.id == reloaded_task.id
    assert task_with_members.name == reloaded_task.name
    assert task_with_members.description == reloaded_task.description
    assert task_with_members.priority == reloaded_task.priority
    assert task_with_members.status == reloaded_task.status
    assert task_with_members.members == reloaded_task.members
    assert task_with_members.history == reloaded_task.history
    assert task_with_members.comments == reloaded_task.comments
    assert task_with_members.start_time == reloaded_task.start_time
    assert task_with_members.end_time == reloaded_task.end_time


def test_error_if_intializing_with_invalid_id(clear_task_instances):
    with pytest.raises(ValueError):
        Task(id='nonexistent_id')


def test_task_eq(clear_task_instances, task_with_members):
    task = task_with_members
    copy_task = Task(id = task.id)
    assert task.id == copy_task.id

def test_task_hash():
    task1 = Task(name="Task 1", description="Description 1")
    task2 = Task(id=task1.id, name="Task 2", description="Description 2")
    task3 = Task(name="Task 3", description="Description 3")

    assert hash(task1) == hash(task2)
    assert hash(task1) != hash(task3)
    
    task_set = {task1, task3}
    assert task1 in task_set
    assert task3 in task_set
    assert task2 in task_set

    task_dict = {task1: "First task", task3: "Second task"}
    assert task_dict[task1] == "First task"
    assert task_dict[task2] == "First task"
    assert task_dict[task3] == "Second task"


def test_task_properties(clear_task_instances, task_with_members, user3):
    task_with_members.name = "Updated Task Name"
    assert task_with_members.name == "Updated Task Name"

    task_with_members.description = "Updated Description"
    assert task_with_members.description == "Updated Description"

    new_start_time = datetime.now() + timedelta(days=1)
    task_with_members.start_time = new_start_time
    assert task_with_members.start_time == new_start_time

    new_end_time = datetime.now() + timedelta(days=2)
    task_with_members.end_time = new_end_time
    assert task_with_members.end_time == new_end_time

    task_with_members.priority = Priority.HIGH
    assert task_with_members.priority == Priority.HIGH

    task_with_members.status = Status.DONE
    assert task_with_members.status == Status.DONE

    task_with_members.members = {user3}
    assert task_with_members.members == {user3}


def test_task_exists(clear_task_instances, empty_task):
    task = empty_task
    assert Task.exists(task.id)
    assert Task.exists(task)
    assert not Task.exists("nonexistent_id")


@patch('base.load_data', MagicMock(return_value=sample_tasks))
def test_load_from_file(clear_task_instances):
    Task.load_from_file()
    assert Task.instances == sample_tasks


@patch('base.save_data')
def test_dump_to_file(mock_save_data, clear_task_instances):
    Task.instances = sample_tasks
    Task.dump_to_file()
    mock_save_data.assert_called_once_with(sample_tasks, TASKS_FILE_PATH)


def test_has_member(clear_task_instances, empty_task, task_with_members, user1):
    task = empty_task
    assert not task.has_member(user1)
    task = task_with_members
    assert task.has_member(user1)


def test_task_add_member(clear_task_instances, empty_task, user1):
    task = empty_task
    task.add_member(user1)
    assert user1 in task.members
    with pytest.raises(ValueError):
        task.add_member(user1)


def test_task_remove_member(clear_task_instances, task_with_members, user1):
    task = task_with_members
    task.remove_member(user1)
    assert user1 not in task.members
    with pytest.raises(ValueError):
        task.remove_member(user1)

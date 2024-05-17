import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
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
def clear_instances():
    """Fixture to clear instances before and after each test"""
    Project.instances.clear()
    User.instances.clear()
    Task.instances.clear()
    yield
    User.instances.clear()
    Task.instances.clear()
    Project.instances.clear()


@pytest.fixture
def empty_task():
    return Task(name="Task Name", description="Task Description")


@pytest.fixture
def task_with_members():
    user1 = User(username="user1", name="User One",
                 email="user1@example.com", password="password")
    task = Task(name="New Task", description="New Description",
                priority=Priority.MEDIUM, status=Status.TODO, members={user1})
    return task, user1


@pytest.fixture
def userfactory():
    def user():
        return User(username=f"user_{uuid.uuid4()}", name="User",
                    email="member@example.com", password="password")
    return user


def test_task_initialization_with_parameters(clear_instances, task_with_members):
    task, user1 = task_with_members
    assert task.id in Task.instances

    assert Task.instances[task.id]['name'] == "New Task"
    assert task.name == "New Task"

    assert Task.instances[task.id]['description'] == "New Description"
    assert task.description == "New Description"

    assert Task.instances[task.id]['priority'] == "MEDIUM"
    assert task.priority == Priority.MEDIUM

    assert Task.instances[task.id]['status'] == "TODO"
    assert task.status == Status.TODO

    assert Task.instances[task.id]['members'] == [user1.username]
    assert task.members == {user1}

    assert Task.instances[task.id]['history'] == []
    assert task.history == []

    assert Task.instances[task.id]['comments'] == []
    assert task.comments == []

    assert isinstance(task.start_time, datetime)
    assert isinstance(task.end_time, datetime)


def test_task_reintialization_with_id(clear_instances, task_with_members):
    task, _ = task_with_members
    reloaded_task = Task(id=task.id)
    assert task.id == reloaded_task.id
    assert task.name == reloaded_task.name
    assert task.description == reloaded_task.description
    assert task.priority == reloaded_task.priority
    assert task.status == reloaded_task.status
    assert task.members == reloaded_task.members
    assert task.history == reloaded_task.history
    assert task.comments == reloaded_task.comments
    assert task.start_time == reloaded_task.start_time
    assert task.end_time == reloaded_task.end_time


def test_error_if_intializing_with_invalid_id(clear_instances):
    with pytest.raises(ValueError):
        Task(id='nonexistent_id')


def test_task_eq(clear_instances, task_with_members):
    task, _ = task_with_members
    copy_task = Task(id=task.id)
    assert task == copy_task


def test_task_hash():
    task1 = Task(name="Task 1", description="Description 1")
    task2 = Task(id=task1.id, name="Task 2", description="Description 2")
    task3 = Task(name="Task 3", description="Description 3")

    assert hash(task1) == hash(task2)
    assert hash(task1) != hash(task3)


def test_task_properties(clear_instances, task_with_members, userfactory):
    task , _ = task_with_members
    task.name = "Updated Task Name"
    assert task.name == "Updated Task Name"

    task.description = "Updated Description"
    assert task.description == "Updated Description"

    new_start_time = datetime.now() + timedelta(days=1)
    task.start_time = new_start_time
    assert task.start_time == new_start_time

    new_end_time = datetime.now() + timedelta(days=2)
    task.end_time = new_end_time
    assert task.end_time == new_end_time

    task.priority = Priority.HIGH
    assert task.priority == Priority.HIGH

    task.status = Status.DONE
    assert task.status == Status.DONE

    user = userfactory() 
    task.members = {user}
    assert task.members == {user}


def test_task_exists(clear_instances, empty_task):
    task = empty_task
    assert Task.exists(task.id)
    assert Task.exists(task)
    assert not Task.exists("nonexistent_id")


@patch('base.load_data', MagicMock(return_value=sample_tasks))
def test_load_task_from_file(clear_instances):
    Task.load_from_file()
    assert Task.instances == sample_tasks


@patch('base.save_data')
def test_dump_task_to_file(mock_save_data, clear_instances):
    Task.instances = sample_tasks
    Task.dump_to_file()
    mock_save_data.assert_called_once_with(sample_tasks, TASKS_FILE_PATH)


def test_task_has_member(clear_instances, empty_task, task_with_members, userfactory):
    task = empty_task
    assert not task.has_member(userfactory())
    task , user1 = task_with_members
    assert task.has_member(user1)


def test_task_add_member(clear_instances, empty_task, userfactory):
    task = empty_task
    user1 = userfactory()
    task.add_member(user1)
    assert user1 in task.members
    with pytest.raises(ValueError):
        task.add_member(user1)


def test_task_remove_member(clear_instances, task_with_members):
    task, user1 = task_with_members
    task.remove_member(user1)
    assert user1 not in task.members
    with pytest.raises(ValueError):
        task.remove_member(user1)

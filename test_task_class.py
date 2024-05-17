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
def advanced_task():
    user1 = User(username="user1", name="User One",
                 email="user1@example.com", password="password")
    task = Task(name="New Task", description="New Description",
                priority=Priority.MEDIUM, status=Status.TODO, members={user1})
    return task, user1, task.start_time, task.end_time


@pytest.fixture
def userfactory():
    def user():
        return User(username=f"user_{uuid.uuid4()}", name="User",
                    email="member@example.com", password="password")
    return user


def validate_task_properties(task, name, description, priority,
                             status, members, start_time, end_time):
    assert task.id in Task.instances

    assert Task.instances[task.id]['name'] == name
    assert task.name == name

    assert Task.instances[task.id]['description'] == description
    assert task.description == description

    assert Task.instances[task.id]['priority'] == priority.name
    assert task.priority == priority

    assert Task.instances[task.id]['status'] == status.name
    assert task.status == status

    assert Task.instances[task.id]['members'] == [
        member.username for member in members]
    assert task.members == set(members)

    assert Task.instances[task.id]['history'] == []
    assert task.history == []

    assert Task.instances[task.id]['comments'] == []
    assert task.comments == []

    assert task.start_time == start_time
    assert task.end_time == end_time


def test_task_initialization_with_default_parameters(clear_instances):
    task = Task()
    validate_task_properties(task, '', '', Priority.LOW, Status.BACKLOG,
                             [], task.start_time, task.end_time)


def test_task_initialization_with_custom_parameters(clear_instances, advanced_task):
    task, user1, st, ed = advanced_task
    validate_task_properties(task, 'New Task', 'New Description',
                             Priority.MEDIUM, Status.TODO, [user1], st, ed)


def test_task_reintialization_with_id(clear_instances, advanced_task):
    task, _, _, _ = advanced_task
    reloaded_task = Task(id=task.id)
    validate_task_properties(reloaded_task, task.name, task.description, task.priority,
                             task.status, task.members, task.start_time, task.end_time)


def test_error_if_intializing_with_invalid_id(clear_instances):
    with pytest.raises(ValueError):
        Task(id='nonexistent_id')


def test_task_eq(clear_instances, advanced_task):
    task, _, _, _ = advanced_task
    copy_task = Task(id=task.id)
    other_task = Task()
    assert task == copy_task
    assert task != other_task


def test_task_hash():
    task1 = Task(name="Task 1", description="Description 1")
    task2 = Task(id=task1.id, name="Task 2", description="Description 2")
    task3 = Task(name="Task 3", description="Description 3")

    assert hash(task1) == hash(task2)
    assert hash(task1) != hash(task3)


def test_task_properties(clear_instances, advanced_task, userfactory):
    task, _, _, _ = advanced_task
    task.name = "Updated Task Name"
    task.description = "Updated Description"
    task.start_time = new_start_time = datetime.now() + timedelta(days=1)
    task.end_time = new_end_time = datetime.now() + timedelta(days=2)
    task.priority = Priority.HIGH
    task.status = Status.DONE
    user = userfactory()
    task.members = {user}
    validate_task_properties(task, "Updated Task Name", "Updated Description", Priority.HIGH,
                             Status.DONE, {user}, new_start_time, new_end_time)


def test_task_exists(clear_instances):
    task = Task()
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


def test_task_has_member(clear_instances, advanced_task, userfactory):
    task = Task()
    assert not task.has_member(userfactory())
    task, user1, _, _ = advanced_task
    assert task.has_member(user1)


def test_task_add_member(clear_instances, userfactory):
    task = Task()
    user1 = userfactory()
    task.add_member(user1)
    assert user1 in task.members
    with pytest.raises(ValueError):
        task.add_member(user1)


def test_task_remove_member(clear_instances, advanced_task):
    task, user1, _, _ = advanced_task
    task.remove_member(user1)
    assert user1 not in task.members
    with pytest.raises(ValueError):
        task.remove_member(user1)

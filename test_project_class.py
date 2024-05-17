import pytest
from unittest.mock import patch, MagicMock
from base import *


@pytest.fixture
def clear_project_instances():
    """Fixture to clear Project.instances before and after each test"""
    Project.instances.clear()
    yield
    Project.instances.clear()


@pytest.fixture
def user():
    return User(username=f"user_{uuid.uuid4()}", name="User",
                email="member@example.com", password="password")


@pytest.fixture
def empty_project():
    leader_user = User(username="leader", name="User Leader",
                       email="leader@example.com", password="password")
    proj = Project('id', 'title', leader_user)
    return {'leader': leader_user, 'project': proj}


@pytest.fixture
def not_empty_project():
    member_user = User(username="member", name="User Member",
                       email="member@example.com", password="password")
    leader_user = User(username="leader", name="User Leader",
                       email="leader@example.com", password="password")
    task = Task()
    proj = Project('id', 'title', leader_user, {member_user}, {task})
    return {'member': member_user, 'leader': leader_user, 'task': task, 'project': proj}
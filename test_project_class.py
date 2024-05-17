import pytest
from unittest.mock import patch, MagicMock, call
from base import *

sample_projects = {
    "1": {
        "title": "Project 1",
        "leader": "Leader1 ID",
        "members": ['Member1.1 ID', 'Member1.2 ID'],
        "tasks": ['Task1.1 ID', 'Task1.2 ID']
    },
    "2": {
        "title": "Project 2",
        "leader": "Leader2 ID",
        "members": ['Member2.1 ID', 'Member2.2 ID'],
        "tasks": ['Task2.1 ID', 'Task2.2 ID']
    }
}


@pytest.fixture
def clear_project_instances():
    """Fixture to clear Project.instances before and after each test"""
    Project.instances.clear()
    yield
    Project.instances.clear()


@pytest.fixture
def userfactory():
    def user():
        return User(username=f"user_{uuid.uuid4()}", name="User",
                    email="member@example.com", password="password")
    return user


@pytest.fixture
def empty_project():
    leader = User(username="leader", name="User Leader",
                  email="leader@example.com", password="password")
    proj = Project(id='id', leader=leader)
    return proj, leader


@pytest.fixture
def not_empty_project():
    member = User(username="member", name="User Member",
                  email="member@example.com", password="password")
    leader = User(username="leader", name="User Leader",
                  email="leader@example.com", password="password")
    task = Task()
    proj = Project('id', 'title', leader, {member}, {task})
    return proj, leader, member, task


def test_project_intialization_with_default_parameters(clear_project_instances, empty_project):
    proj, leader = empty_project
    assert proj.id in Project.instances

    assert Project.instances[proj.id]['title'] == None
    assert proj.title == None

    assert Project.instances[proj.id]['leader'] == leader.username
    assert proj.leader == leader

    assert Project.instances[proj.id]['members'] == []
    assert proj.members == set()

    assert Project.instances[proj.id]['tasks'] == []
    assert proj.tasks == set()


def test_project_intialization_with_custom_parameters(clear_project_instances, not_empty_project):
    proj, leader, member, task = not_empty_project

    assert proj.id in Project.instances

    assert Project.instances[proj.id]['title'] == 'title'
    assert proj.title == 'title'

    assert Project.instances[proj.id]['leader'] == leader.username
    assert proj.leader == leader

    assert Project.instances[proj.id]['members'] == [member.username]
    assert proj.members == {member}

    assert Project.instances[proj.id]['tasks'] == [task.id]
    assert proj.tasks == {task}


def test_project_reinitialization_with_id(clear_project_instances, not_empty_project):
    proj, _, _, _ = not_empty_project
    reloaded_proj = Project(id=proj.id)

    assert reloaded_proj.id == proj.id
    assert reloaded_proj.title == proj.title
    assert reloaded_proj.leader == proj.leader
    assert reloaded_proj.members == proj.members
    assert reloaded_proj.tasks == proj.tasks


def test_error_if_intializing_with_invalid_id_without_leader(clear_project_instances):
    with pytest.raises(ValueError):
        Project(id='nonexistent_id')


def test_project_eq(clear_project_instances, not_empty_project):
    proj, _, _, _ = not_empty_project
    copy_proj, _, _, _ = not_empty_project
    assert proj == copy_proj


def test_project_hash(clear_project_instances, not_empty_project, userfactory):
    proj1, _, _, _ = not_empty_project
    proj2 = Project(id=proj1.id)
    leader = userfactory()
    proj3 = Project(id=f"{proj1.id}2", leader=leader)

    hash(proj1) == hash(proj2)
    hash(proj1) != hash(proj3)


def test_project_properties(clear_project_instances, not_empty_project, userfactory):
    proj, _, _, _ = not_empty_project
    proj.name = "Updated Project Name"
    assert proj.name == "Updated Project Name"

    proj.title = "Updated Title"
    assert proj.title == "Updated Title"

    new_leader = userfactory()
    proj.leader = new_leader
    assert proj.leader == new_leader

    new_member = userfactory()
    proj.members = {new_member}
    assert proj.members == {new_member}

    new_task = Task()
    proj.tasks = {new_task}
    assert proj.tasks == {new_task}


def test_project_exists(clear_project_instances, not_empty_project):
    proj, _, _, _ = not_empty_project
    assert Project.exists(proj)
    assert Project.exists(proj.id)
    assert not Project.exists("nonexistent_id")


@patch('base.load_data', MagicMock(return_value=sample_projects))
def test_load_project_from_file(clear_project_instances):
    Project.load_from_file()
    assert Project.instances == sample_projects


@patch('base.save_data')
def test_dump_project_to_file(mock_save_data, clear_project_instances):
    Project.instances = sample_projects
    Project.dump_to_file()
    mock_save_data.assert_called_once_with(sample_projects, PROJECTS_FILE_PATH)


def test_project_has_member(clear_project_instances, not_empty_project, userfactory):
    proj, leader, member, _ = not_empty_project
    unrelated_user = userfactory()

    assert proj.has_member(member)
    assert not proj.has_member(leader)
    assert not proj.has_member(unrelated_user)


def test_project_is_leader(clear_project_instances, not_empty_project, userfactory):
    proj, leader, member, _ = not_empty_project
    unrelated_user = userfactory()

    assert proj.is_leader(leader)
    assert not proj.is_leader(member)
    assert not proj.is_leader(unrelated_user)


def test_project_task_belongs(clear_project_instances, not_empty_project):
    proj, _, _, belonging_task = not_empty_project
    unrelated_task = Task()

    assert proj.task_belongs(belonging_task)
    assert not proj.task_belongs(unrelated_task)


def test_project_remove(clear_project_instances, not_empty_project):
    proj, leader, member, task = not_empty_project
    proj.remove()

    assert proj.id not in Project.instances
    assert proj not in leader.leading
    assert proj not in member.involved
    assert task.id not in Task.instances


def test_project_add_member(clear_project_instances, userfactory, empty_project):
    proj, _ = empty_project
    user = userfactory()
    proj.add_member(user)
    assert user in proj.members
    assert proj in user.involved
    with pytest.raises(ValueError):
        proj.add_member(user)


def test_project_remove_member(clear_project_instances, not_empty_project):
    proj, leader, member, _ = not_empty_project
    proj.remove_member(member)
    assert member not in proj.members
    assert proj not in member.involved
    with pytest.raises(ValueError):
        proj.remove_member(member)
    with pytest.raises(ValueError):
        proj.remove_member(leader)


def test_project_add_task(clear_project_instances, empty_project):
    proj, _ = empty_project
    task = Task()

    proj.add_task(task)
    assert task in proj.tasks
    with pytest.raises(ValueError):
        proj.add_task(task)


def test_project_remove_task(clear_project_instances, not_empty_project):
    proj, _, _, task = not_empty_project
    another_task = Task()
    proj.remove_task(task)

    assert task not in proj.tasks
    assert task.id not in Task.instances
    with pytest.raises(ValueError):
        proj.remove_task(task)
    with pytest.raises(ValueError):
        proj.remove_task(another_task)


def test_project_add_member_to_task(clear_project_instances, not_empty_project, userfactory):
    proj, member, leader, task = not_empty_project
    unrelated_user = userfactory()
    unrelated_task = Task()

    with patch.object(task, 'add_member') as mock_add_member:
        proj.add_member_to_task(member, task)
        proj.add_member_to_task(member, task, True)
        proj.add_member_to_task(leader, task)
        proj.add_member_to_task(leader, task, True)
        expected_calls = [call(member, False), call(member, True),
                          call(leader, False), call(leader, True)]
        mock_add_member.assert_has_calls(expected_calls, any_order=False)

    proj.add_member_to_task(leader, task)
    assert leader in task.members
    proj.add_member_to_task(member, task)
    assert member in task.members

    with pytest.raises(ValueError):
        proj.add_member_to_task(leader, task)
    with pytest.raises(ValueError):
        proj.add_member_to_task(member, task)

    with pytest.raises(ValueError):
        proj.add_member_to_task(unrelated_user, task)
    with pytest.raises(ValueError):
        proj.add_member_to_task(member, unrelated_task)


def test_project_remove_member_from_task(clear_project_instances, not_empty_project):
    proj, leader, member, task = not_empty_project
    proj.add_member_to_task(member, task)
    proj.add_member_to_task(leader, task)

    with patch.object(task, 'remove_member') as mock_remove_member:
        proj.remove_member_from_task(member, task)
        proj.remove_member_from_task(member, task, True)
        proj.remove_member_from_task(leader, task)
        proj.remove_member_from_task(leader, task, True)
        expected_calls = [call(member, False), call(member, True),
                          call(leader, False), call(leader, True)]
        mock_remove_member.assert_has_calls(expected_calls, any_order=False)

    proj.remove_member_from_task(member, task)
    assert member not in task.members
    proj.remove_member_from_task(leader, task)
    assert leader not in task.members

    with pytest.raises(ValueError):
        proj.remove_member_from_task(member, task)
    with pytest.raises(ValueError):
        proj.remove_member_from_task(leader, task)
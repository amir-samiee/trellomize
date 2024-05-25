import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from test_project_class import clear_instances, basic_project, userfactory
sys.path.append(str(Path.cwd()))
from base import *

sample_users = {
    "janesmth": {
        "name": "Jane Smith",
        "email": "janesmith33@gmail.com",
        "password": "gAAAAABmRQt-mpYi3gUPY4EhHNj22K2WXhsdzVYnyaDTc2qf_LXuaijIGs7rJb1y0a-Cvxevv3GZMJH3CeqdIudlb3YkgBRcmQ==",
        "is_active": True,
        "leading": [
            "newProject"
        ],
        "involved": []
    },
    "alexb": {
        "name": "Alex Brown",
        "email": "alexb@gmail.com",
        "password": "gAAAAABmRlagHX_qJr_uwOnsUUfbt1cqSpW7zDXSIwwfvinj9Ivi9ZRIjRXRWwF-EKrhMCFJ6qnu3fkZosGnaSsqbOljEd7VmQ==",
        "is_active": True,
        "involved": [
            "newProject"
        ],
        "leading": []
    }
}


@pytest.fixture
def basic_user():
    return User('user', password='password', is_active=True)


@pytest.fixture
def advanced_user():
    proj1 = Project('id1', 'title1', User('leaderer', password='password'))
    user = User('user', 'name', 'user@example.com',
                'password', True, {proj1}, {})
    proj2 = Project('id2', 'title2', user)
    return user, proj1, proj2


def validate_user_parameters(user, username, password, name='', email='', active=True, leading=[], involved=[]):
    assert user.username in User.instances
    assert user.username == username

    assert User.instances[user.username]['name'] == name
    assert user.name == name

    assert User.instances[user.username]['email'] == email
    assert user.email == email

    assert User.instances[user.username]['password'] == password
    assert user.password == password

    assert User.instances[user.username]['is_active'] == active
    assert user.is_active == active

    assert User.instances[user.username]['leading'] == [p.id for p in leading]
    assert user.leading == set(leading)

    assert User.instances[user.username]['involved'] == [
        p.id for p in involved]
    assert user.involved == set(involved)


def test_user_intialization_with_default_parameters(clear_instances, basic_user):
    validate_user_parameters(basic_user, 'user', 'password')


def test_intialization_with_custom_parameters(clear_instances, advanced_user):
    user, involved_proj, leading_proj = advanced_user
    validate_user_parameters(user, 'user', 'password', 'name',
                             'user@example.com', True, [leading_proj], [involved_proj])


def test_reintialization_with_username(clear_instances, basic_user):
    user = basic_user
    reloaded_user = User(username=user.username)
    validate_user_parameters(reloaded_user, user.username, user.password,
                             user.name, user.email, user.is_active, user.leading, user.involved)


def test_error_if_intialized_with_invalid_username(clear_instances):
    with pytest.raises(ValueError):
        User(username='nonexistent_username')


def test_user_eq(clear_instances, userfactory):
    user1 = userfactory()
    user2 = User(username=user1.username)
    user3 = userfactory()
    assert user1 == user2
    assert user1 != user3


def test_user_hash(clear_instances, userfactory):
    user1 = userfactory()
    user2 = User(username=user1.username)
    user3 = userfactory()

    assert hash(user1) == hash(user2)
    assert hash(user1) != hash(user3)


def test_user_str(clear_instances, basic_user):
    assert str(basic_user) == basic_user.username


def test_user_properties(clear_instances, basic_user, basic_project):
    proj, _ = basic_project
    proj2 = Project('idd', 'title', leader=basic_user)
    basic_user.name = 'newname'
    basic_user.email = 'newmail@example.com'
    basic_user.password = 'newpass'
    basic_user.is_active = False
    basic_user.leading = [proj2]
    basic_user.involved = [proj]
    validate_user_parameters(basic_user, basic_user.username, 'newpass', 'newname',
                             'newmail@example.com', False, [proj2], [proj])


def test_user_exists_test(clear_instances, basic_user):
    assert User.exists(basic_user)
    assert User.exists(basic_user.username)
    assert not User.exists(f"not{basic_user.username}")


@patch('base.handeled_load_data', MagicMock(return_value=sample_users))
def test_load_user_from_file(clear_instances):
    User.load_from_file()
    assert User.instances == sample_users


@patch('base.save_data')
def test_save_user_to_file(mock_save_data, clear_instances):
    User.instances = sample_users
    User.dump_to_file()
    mock_save_data.assert_called_once_with(sample_users, USERS_FILE_PATH)

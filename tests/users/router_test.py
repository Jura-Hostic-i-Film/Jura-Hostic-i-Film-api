from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.users import UserService
from app.utils.exceptions.user_exceptions import UserException
from tests.users.util import user, user_jwt, admin, admin_jwt, user_create

client = TestClient(app)


# Not Authenticated
def test_get_all_users_not_authenticated():
    response = client.get("/users/")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

"""
def test_register_not_authenticated():
    response = client.post("/users/register", json=user_create)
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}
"""

def test_get_me_not_authenticated():
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}


# Not Authorized
def test_get_all_users_not_authorized():
    response = client.get("/users/", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_register_not_authorized():
    response = client.post("/users/register", headers={"Authorization": f"Bearer {user_jwt}"}, json=user_create.model_dump())
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


# Success
def test_get_all_users():
    mock_user_service = Mock(spec=UserService)
    mock_user_service.get_all_users.return_value = [user.model_dump()]

    with patch("app.routers.users.UserService", return_value=mock_user_service):
        response = client.get("/users/", headers={"Authorization": f"Bearer {admin_jwt}"})

    mock_user_service.get_all_users.assert_called_once()

    assert response.status_code == 200
    assert response.json() == mock_user_service.get_all_users.return_value


def test_register():
    mock_user_service = Mock(spec=UserService)
    mock_user_service.register_user.return_value = user.model_dump()

    with patch("app.routers.users.UserService", return_value=mock_user_service):
        response = client.post("/users/register", headers={"Authorization": f"Bearer {admin_jwt}"}, json=user_create.model_dump())

    mock_user_service.register_user.assert_called_once()

    assert response.status_code == 200
    assert response.json() == mock_user_service.register_user.return_value


def test_get_me():
    mock_user_service = Mock(spec=UserService)
    mock_user_service.get_user.return_value = user.model_dump()

    with patch("app.routers.users.UserService", return_value=mock_user_service):
        response = client.get("/users/me", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_user_service.get_user.assert_called_once()

    assert response.status_code == 200
    assert response.json() == mock_user_service.get_user.return_value


def test_register_admin():
    mock_user_service = Mock(spec=UserService)
    mock_user_service.register_admin.return_value = admin.model_dump()

    with patch("app.routers.users.UserService", return_value=mock_user_service):
        response = client.post("/users/register/admin", json=user_create.model_dump())

    mock_user_service.register_admin.assert_called_once()

    assert response.status_code == 200
    assert response.json() == mock_user_service.register_admin.return_value


def test_login():
    mock_user_service = Mock(spec=UserService)
    mock_user_service.login_user.return_value = {"token": user_jwt}

    with patch("app.routers.users.UserService", return_value=mock_user_service):
        response = client.post("/users/login", json={"username": "test", "password": "test"})

    mock_user_service.login_user.assert_called_once()

    assert response.status_code == 200
    assert response.json() == mock_user_service.login_user.return_value


# Error cases
def test_register_username_exists():
    mock_user_service = Mock(spec=UserService)
    mock_user_service.register_user.side_effect = UserException.UserAlreadyExists({"username": "test"})

    with patch("app.routers.users.UserService", return_value=mock_user_service):
        response = client.post("/users/register", headers={"Authorization": f"Bearer {admin_jwt}"}, json=user_create.model_dump())

    mock_user_service.register_user.assert_called_once()

    assert response.status_code == 409
    assert response.json() == {'app_exception': 'UserAlreadyExists', 'context': {'username': 'test'}}


def test_register_director_exists():
    mock_user_service = Mock(spec=UserService)
    mock_user_service.register_user.side_effect = UserException.DirectorAlreadyExists({})

    with patch("app.routers.users.UserService", return_value=mock_user_service):
        response = client.post("/users/register", headers={"Authorization": f"Bearer {admin_jwt}"}, json=user_create.model_dump())

    mock_user_service.register_user.assert_called_once()

    assert response.status_code == 409
    assert response.json() == {'app_exception': 'DirectorAlreadyExists', 'context': {}}

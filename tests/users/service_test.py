from unittest.mock import Mock, patch

from app.services.users import UserService
from tests.users.util import user, user_create


def test_register_user():
    mock_user_crud = Mock()
    mock_user_crud.create_user.return_value = user.model_dump()
    mock_user_crud.get_users_by_role.return_value = None
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.register_user(user_create)

    mock_user_crud.create_user.assert_called_once_with(user_create)
    mock_user_crud.get_users_by_role.assert_not_called()
    assert result == user.model_dump()


def test_get_users():
    mock_user_crud = Mock()
    mock_user_crud.get_all.return_value = [user.model_dump()]
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.get_users()

    mock_user_crud.get_all.assert_called_once()
    assert result == [user.model_dump()]


def test_delete_user():
    mock_user_crud = Mock()
    mock_user_crud.delete_user.return_value = user.model_dump()
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.delete_user("username")

    mock_user_crud.delete_user.assert_called_once_with("username")
    assert result == user.model_dump()


def test_update_user():
    mock_user_crud = Mock()
    mock_user_crud.update_user.return_value = user.model_dump()
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.update_user("username", user_create)

    mock_user_crud.update_user.assert_called_once_with("username", user_create)
    assert result == user.model_dump()


def test_update_user_password():
    mock_user_crud = Mock()
    mock_user_crud.update_user_password.return_value = True
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.update_user_password("username", "new_password")

    mock_user_crud.update_user_password.assert_called_once_with("username", "new_password")
    assert result == True


def test_get_user():
    mock_user_crud = Mock()
    mock_user_crud.get_user.return_value = user.model_dump()
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.get_user("username")

    mock_user_crud.get_user.assert_called_once_with("username")
    assert result == user.model_dump()


def test_register_admin():
    mock_user_crud = Mock()
    mock_user_crud.get_users_by_role.return_value = None
    mock_user_crud.create_user.return_value = user.model_dump()
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.register_admin(user_create)

    mock_user_crud.create_user.assert_called_once_with(user_create)
    assert result == user.model_dump()


def test_admin_exists():
    mock_user_crud = Mock()
    mock_user_crud.get_users_by_role.return_value = [user.model_dump()]
    db = Mock()

    user_service = UserService(db)

    with patch("app.services.users.UserCRUD", return_value=mock_user_crud):
        result = user_service.admin_exists()

    mock_user_crud.get_users_by_role.assert_called_once_with("admin")
    assert result == True

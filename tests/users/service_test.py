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
from app.config.jwt import access_security
from app.schemas.users import User, Role, UserCreate
from app.utils.enums import RolesEnum

user = User(
    id=1,
    email="test@email.com",
    first_name="Test",
    last_name="Test",
    username="test",
    roles=[],
)
user_jwt = access_security.create_access_token(subject={"username": user.username, "roles": user.roles})
admin = User(
    id=1,
    email="test@email.com",
    first_name="Test",
    last_name="Test",
    username="test",
    roles=[Role(name=RolesEnum.ADMIN)],
)
admin_jwt = access_security.create_access_token(subject={"username": admin.username, "roles": [RolesEnum.ADMIN]})
director = User(
    id=1,
    email="test@email.com",
    first_name="Test",
    last_name="Test",
    username="test",
    roles=[Role(name=RolesEnum.DIRECTOR)],
)
director_jwt = access_security.create_access_token(
    subject={"username": director.username, "roles": [RolesEnum.DIRECTOR]})
user_create = UserCreate(
    email="mail@mail.com",
    first_name="Test",
    last_name="Test",
    username="test",
    password="test",
    roles=[RolesEnum.ADMIN],
)

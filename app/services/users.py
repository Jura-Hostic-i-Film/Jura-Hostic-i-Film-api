from typing import Type

from app.config.jwt import access_security
from app.models.users import UserDB, RoleDB
from app.schemas.users import UserCreate, User, AccessToken
from app.services.main import AppService, AppCRUD
from app.utils.enums import RolesEnum
from app.utils.exceptions.user_exceptions import UserException
from app.utils.password_hash import verify_password, hash_password


class UserService(AppService):
    def register_user(self, user: UserCreate) -> User:
        if RolesEnum.DIRECTOR in user.roles:
            director = UserCRUD(self.db).get_users_by_role("director")
            if director:
                raise UserException.DirectorAlreadyExists({})

        user = UserCRUD(self.db).create_user(user)

        return user

    def login_user(self, username: str, password: str) -> AccessToken:
        user = UserCRUD(self.db).get_user(username)
        if not user:
            raise UserException.UserNotFound({"username": username})
        if not verify_password(password, user.password):
            raise UserException.InvalidPassword({"username": username})

        roles = []
        for role in user.roles:
            roles.append(role.name)

        subject = {"username": user.username, "roles": roles}

        access_token = access_security.create_access_token(subject=subject)

        return AccessToken(token=access_token)

    def get_user(self, username: str) -> User:
        user = UserCRUD(self.db).get_user(username)
        if not user:
            raise UserException.UserNotFound({"username": username})

        return user

    def get_users(self, roles: list[RolesEnum] | None = None) -> list[User]:

        if roles:
            users_db = []
            for role in roles:
                users_db += UserCRUD(self.db).get_users_by_role(role.value)
        else:
            users_db = UserCRUD(self.db).get_all()

        return users_db

    def register_admin(self, user: UserCreate) -> User:
        if RolesEnum.ADMIN not in user.roles:
            user.roles.append(RolesEnum.ADMIN)

        admins = UserCRUD(self.db).get_users_by_role("admin")

        if admins:
            raise UserException.AdminAlreadyExists({})

        return self.register_user(user)

    def admin_exists(self) -> bool:
        admins = UserCRUD(self.db).get_users_by_role("admin")

        if admins:
            return True
        return False

    def delete_user(self, username: str) -> User:
        return UserCRUD(self.db).delete_user(username)

    def update_user(self, username: str, user: User) -> User:
        return UserCRUD(self.db).update_user(username, user)

    def update_user_password(self, username: str, password: str) -> bool:
        user = UserCRUD(self.db).update_user_password(username, password)

        return user

    def get_user_by_id(self, user_id: int) -> User:
        return UserCRUD(self.db).get_user_by_id(user_id)


class UserCRUD(AppCRUD):
    def create_user(self, user: UserCreate) -> UserDB:
        roles = []

        user_db = self.db.query(UserDB).filter(UserDB.username == user.username).first()
        if user_db:
            raise UserException.UserAlreadyExists({"username": user.username})

        user_db = self.db.query(UserDB).filter(UserDB.email == user.email).first()
        if user_db:
            raise UserException.UserAlreadyExists({"email": user.email})

        for role in user.roles:
            role_db = self.db.query(RoleDB).filter(RoleDB.name == role).first()
            if not role_db:
                raise UserException.InvalidRole({"role": role})
            roles.append(role_db)

        userdb = UserDB(
            username=user.username,
            password=hash_password(user.password),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=roles
        )
        self.db.add(userdb)
        self.db.commit()
        self.db.refresh(userdb)
        return userdb

    def get_user(self, username: str) -> UserDB:
        return self.db.query(UserDB).filter(UserDB.username == username).first()

    def get_all(self) -> list[Type[UserDB]]:
        return self.db.query(UserDB).all()

    def get_users_by_role(self, role: str) -> list[Type[UserDB]]:
        return self.db.query(UserDB).filter(UserDB.roles.any(name=role)).all()

    def delete_user(self, username: str) -> UserDB:
        user = self.db.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            raise UserException.UserNotFound({"username": username})

        self.db.delete(user)
        self.db.commit()

        return user

    def update_user(self, username: str, user: User) -> UserDB:
        user_db = self.db.query(UserDB).filter(UserDB.username == username).first()
        if not user_db:
            raise UserException.UserNotFound({"username": username})

        user_db.email = user.email
        user_db.first_name = user.first_name
        user_db.last_name = user.last_name
        user_db.username = user.username

        roles = []
        for role in user.roles:
            role_db = self.db.query(RoleDB).filter(RoleDB.name == role).first()
            if not role_db:
                raise UserException.InvalidRole({"role": role})
            roles.append(role_db)

        user_db.roles = roles

        self.db.commit()
        self.db.refresh(user_db)

        return user_db

    def update_user_password(self, username: str, password: str) -> bool:
        user_db = self.db.query(UserDB).filter(UserDB.username == username).first()
        if not user_db:
            raise UserException.UserNotFound({"username": username})

        user_db.password = hash_password(password)

        self.db.commit()
        self.db.refresh(user_db)

        return True

    def get_user_by_id(self, user_id: int) -> UserDB:
        return self.db.query(UserDB).filter(UserDB.id == user_id).first()
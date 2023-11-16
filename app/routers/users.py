from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.schemas.users import UserLogin, UserCreate, User, AccessToken
from app.services.users import UserService
from app.utils.enums import RolesEnum

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_all_users(db: get_db = Depends(),
                        credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[User]:
    result = UserService(db).get_all_users()
    return result


@router.post("/register")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def register(user: UserCreate, db: get_db = Depends(),
                   credentials: JwtAuthorizationCredentials = Security(access_security)) -> User:
    result = UserService(db).register_user(user)
    return result


@router.post("/register/admin")
async def register_admin(user: UserCreate, db: get_db = Depends()) -> User:
    result = UserService(db).register_admin(user)
    return result


@router.get("/me")
@authenticate()
async def me(db: get_db = Depends(), credentials: JwtAuthorizationCredentials = Security(access_security)) -> User:
    username = credentials["username"]
    result = UserService(db).get_user(username)
    return result


@router.post("/login")
async def login(user: UserLogin, db: get_db = Depends()) -> AccessToken:
    result = UserService(db).login_user(user.username, user.password)
    return result


@router.get("/admin/exists")
async def admin_exists(db: get_db = Depends()) -> bool:
    result = UserService(db).admin_exists()
    return bool(result)
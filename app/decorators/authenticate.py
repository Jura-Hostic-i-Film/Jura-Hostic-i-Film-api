from functools import wraps
from typing import List

from app.utils.enums import RolesEnum
from app.utils.exceptions.app_exceptions import AppException

"""
Usage:
from app.decorators.authenticate import authenticate

@router.post("/path") 
@authenticate([RolesEnum.admin, RolesEnum.director])    # needs to be authenticated and have one of the roles
@authenticate()                                         # only needs to be authenticated
async def path(credentials: JwtAuthorizationCredentials = Security(access_security)):
    # do something
"""


def authenticate(required_roles: List[RolesEnum] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            credentials = kwargs.get("credentials")
            if not credentials:
                raise AppException.NotAuthenticated({})

            if required_roles and not any(role in credentials["roles"] for role in required_roles):
                raise AppException.NotAuthorized({})

            return await func(*args, **kwargs)

        return wrapper

    return decorator

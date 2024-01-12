from app.utils.exceptions.app_exceptions import AppExceptionCase


class UserException:
    class UserNotFound(AppExceptionCase):
        def __init__(self, context: dict):
            """
            User not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class InvalidPassword(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Invalid password
            """
            status_code = 400
            AppExceptionCase.__init__(self, status_code, context)

    class UserAlreadyExists(AppExceptionCase):
        def __init__(self, context: dict):
            """
            User already exists
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)

    class AdminAlreadyExists(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Admin already exists
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)

    class DirectorAlreadyExists(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Director already exists
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)

    class InvalidCredentials(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Invalid credentials
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)

    class InvalidRole(AppExceptionCase):
        def __int__(self, context: dict):
            """
            Invalid role
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)


    class NoUsersWithRole(AppExceptionCase):
        def __int__(self, context: dict):
            """
            No users with role
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)
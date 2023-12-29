from app.utils.exceptions.app_exceptions import AppExceptionCase

class AuditException:
    class AuditNotFound(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Audit not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class DocumentAuditAlreadyExists(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document audit already exists
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)


    class DocumentAuditNotFound(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document audit not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)
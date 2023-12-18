from app.utils.exceptions.app_exceptions import AppExceptionCase


class DocumentException:
    class DocumentNotFound(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class DocumentStatusNotProvided(AppExceptionCase):
        def __init__(self):
            """
            Document status not provided
            """
            status_code = 400
            context = {"detail": "Document status not provided"}
            AppExceptionCase.__init__(self, status_code, context)

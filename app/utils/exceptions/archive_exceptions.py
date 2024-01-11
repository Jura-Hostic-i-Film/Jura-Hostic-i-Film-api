from app.utils.exceptions.app_exceptions import AppExceptionCase

class ArchiveException:
    class DocumentArchiveNotFound(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document is not archived
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class DocumentArchiveAlreadyExists(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document already archived
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)

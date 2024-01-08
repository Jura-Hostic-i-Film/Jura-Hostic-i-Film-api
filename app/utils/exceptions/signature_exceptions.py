from app.utils.exceptions.app_exceptions import AppExceptionCase

class SignatureException:
    class DocumentSignatureNotFound(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document is not signed
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class DocumentSignatureAlreadyExists(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document already signed
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)

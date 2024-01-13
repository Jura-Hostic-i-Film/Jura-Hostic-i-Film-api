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

    class DocumentStatusNotCompatible(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Document status not compatible
            """
            status_code = 400
            AppExceptionCase.__init__(self, status_code, context)

    class DocumentNotDetected(AppExceptionCase):
        def __init__(self):
            """
            Document not detected
            """
            status_code = 400
            context = {"detail": "Document not detected"}
            AppExceptionCase.__init__(self, status_code, context)

    class ImageNotFound(AppExceptionCase):
        def __init__(self, context: dict):
            """
            Image not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class ImageUploadFailed(AppExceptionCase):
        def __init__(self):
            """
            Image upload failed
            """
            status_code = 500
            context = {"detail": "Image upload failed"}
            AppExceptionCase.__init__(self, status_code, context)

    class DocumentTypeNotRecognized(AppExceptionCase):
        def __init__(self):
            """
            Document type not recognized
            """
            status_code = 400
            context = {"detail": "Document type not recognized"}
            AppExceptionCase.__init__(self, status_code, context)

from unittest.mock import Mock, patch

from _pytest.python_api import raises

from app.services.documents import DocumentService, ImageService, ImageCRUD
from app.utils.enums import DocumentStatusEnum
from app.utils.exceptions.document_exceptions import DocumentException
from tests.documents.util import document1, document2, documents, uploaded_image, imageDB
from tests.users.util import admin


def test_get_all_documents():
    mock_document_crud = Mock()
    mock_document_crud.get_all_documents.return_value = documents
    db = Mock()

    document_service = DocumentService(db)

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud):
        result = document_service.get_all_documents(None, None)

    mock_document_crud.get_all_documents.assert_called_once()
    assert result == documents


def test_get_documents():
    mock_document_crud = Mock()
    mock_document_crud.get_documents.return_value = documents
    db = Mock()

    document_service = DocumentService(db)

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud):
        result = document_service.get_documents("username")

    mock_document_crud.get_documents.assert_called_once()
    assert result == documents


@patch("app.services.documents.detect_document", return_value="summary")
def test_create_document(detect_document):
    mock_document_crud = Mock()
    mock_document_crud.create_document.return_value = document1

    mock_user_service = Mock()
    mock_user_service.get_user.return_value = admin

    mock_image_service = Mock()
    mock_image_service.create_image.return_value = imageDB
    db = Mock()

    document_service = DocumentService(db)

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud), \
            patch("app.services.documents.ImageService", return_value=mock_image_service), \
            patch("app.services.documents.UserService", return_value=mock_user_service):
        result = document_service.create_document(uploaded_image, "username")

    detect_document.assert_called_once()
    mock_user_service.get_user.assert_called_once()
    mock_image_service.create_image.assert_called_once()

    assert result == document1


def test_get_document():
    mock_document_crud = Mock()
    mock_document_crud.get_document.return_value = document1

    db = Mock()

    document_service = DocumentService(db)

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud):
        result = document_service.get_document(1)

    mock_document_crud.get_document.assert_called_once()

    assert result == document1


def test_get_image():
    mock_image_crud = Mock(spec=ImageCRUD)
    mock_image_crud.get_image.return_value = uploaded_image
    db = Mock()

    image_service = ImageService(db)

    with patch("app.services.documents.ImageCRUD", return_value=mock_image_crud):
        result = image_service.get_image(1)

    mock_image_crud.get_image.assert_called_once()
    assert result == uploaded_image


from unittest.mock import Mock, patch

from _pytest.python_api import raises

from app.services.documents import DocumentService
from app.utils.enums import DocumentStatusEnum
from app.utils.exceptions.document_exceptions import DocumentException
from tests.documents.util import document1, document2, documents, uploaded_image, image


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


def test_create_document():
    mock_document_crud = Mock()
    mock_document_crud.create_document.return_value = document1
    db = Mock()

    document_service = DocumentService(db)

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud):
        result = document_service.create_document(uploaded_image, "username")

    mock_document_crud.create_document.assert_called_once()
    assert result == document1


def test_get_document_and_get_image():
    mock_document_crud = Mock()
    mock_document_crud.get_document.return_value = document1
    mock_document_crud.get_image.return_value = image
    db = Mock()

    document_service = DocumentService(db)

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud):
        result1 = document_service.get_document(1)
        result2 = document_service.get_image(1)

    mock_document_crud.get_document.assert_called_once()
    assert result1 == document1
    assert result2 == image


def test_update_document():
    mock_document_crud = Mock()
    mock_document_crud.get_document.return_value = None
    mock_document_crud.update_document.return_value = document2
    db = Mock()

    document_service = DocumentService(db)

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud):
        assert raises(DocumentException.DocumentNotFound, document_service.update_document, 1, "signed")

    mock_document_crud.get_document.return_value = document2

    with patch("app.services.documents.DocumentCRUD", return_value=mock_document_crud):
        result = document_service.update_document(2, DocumentStatusEnum.SIGNED)

    assert result == document2

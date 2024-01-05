from unittest.mock import Mock, patch
from app.utils.enums import ActionStatus
from app.services.signatures import SignatureService
from tests.signatures.util import signature1, signature2, signatures, signature_create
from _pytest.python_api import raises
from pydantic import BaseModel


def test_get_all_signatures():
    mock_signature_crud = Mock()
    mock_signature_crud.get_all_signatures.return_value = signatures
    db = Mock()

    signature_service = SignatureService(db)

    with patch("app.services.signatures.SignatureCRUD", return_value=mock_signature_crud):
        result = signature_service.get_all_signatures()

    mock_signature_crud.get_all_signatures.assert_called_once()
    assert result == signatures


def test_get_all_pending_signatures():
    mock_signature_crud = Mock()
    mock_signature_crud.get_signatures_by_status.return_value = signatures
    db = Mock()

    signature_service = SignatureService(db)

    with patch("app.services.signatures.SignatureCRUD", return_value=mock_signature_crud):
        result = signature_service.get_all_pending_signatures()

    mock_signature_crud.get_signatures_by_status.assert_called_once_with(ActionStatus.PENDING)
    assert result == signatures


def test_get_all_signed_documents():
    mock_signature_crud = Mock()
    mock_signature_crud.get_signatures_by_status.return_value = signatures
    db = Mock()

    signature_service = SignatureService(db)

    with patch("app.services.signatures.SignatureCRUD", return_value=mock_signature_crud):
        result = signature_service.get_all_signed_documents()

    mock_signature_crud.get_signatures_by_status.assert_called_once_with(ActionStatus.DONE)
    assert result == signatures


def test_sign_document():
    mock_signature_crud = Mock()
    mock_signature_crud.get_signed_by_document_id.return_value = signature1
    mock_signature_crud.update_signature.return_value = True
    db = Mock()

    signature_service = SignatureService(db)

    with patch("app.services.signatures.SignatureCRUD", return_value=mock_signature_crud):
        result = signature_service.sign_document(1)

    mock_signature_crud.get_signed_by_document_id.assert_called_once_with(1)
    mock_signature_crud.update_signature.assert_called_once()
    assert result is True


def test_create_signature():
    mock_signature_crud = Mock()
    mock_signature_crud.create_signature.return_value = signature1
    db = Mock()

    signature_service = SignatureService(db)

    with patch("app.services.signatures.SignatureCRUD", return_value=mock_signature_crud):
        result = signature_service.create_signature_request(signature_create)

    mock_signature_crud.create_signature.assert_called_once_with(signature_create)
    assert result == signature1

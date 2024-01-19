from unittest.mock import Mock, patch
from app.utils.enums import ActionStatus
from app.services.signatures import SignatureService
from tests.signatures.util import signatures


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


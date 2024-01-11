from unittest.mock import Mock, patch

from _pytest.python_api import raises

from app.services.audit import AuditService
from app.utils.exceptions.audit_exceptions import AuditException
from tests.audit.util import audits


def test_get_all_audits():
    mock_audit_crud = Mock()
    mock_audit_crud.get_all_audits.return_value = audits
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.get_all_audits()

    mock_audit_crud.get_all_audits.assert_called_once()
    assert result == audits


def test_get_pending_audits():
    mock_audit_crud = Mock()
    mock_audit_crud.get_audits_by_user_and_status.return_value = audits
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.get_pending_audits("username")

    mock_audit_crud.get_audits_by_user_and_status.assert_called_once()
    assert result == audits


def test_get_audited_documents():
    mock_audit_crud = Mock()
    mock_audit_crud.get_audits_by_user_and_status.return_value = audits
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.get_audited_documents("username")

    mock_audit_crud.get_audits_by_user_and_status.assert_called_once()
    assert result == audits


def test_create_audit_request():
    mock_audit_crud = Mock()
    mock_audit_crud.create_audit.return_value = audits[0]
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.create_audit_request(audits[0])

    mock_audit_crud.create_audit.assert_called_once()
    assert result == audits[0]


def test_get_all_pending_audits():
    mock_audit_crud = Mock()
    mock_audit_crud.get_audits_by_status.return_value = audits
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.get_all_pending_audits()

    mock_audit_crud.get_audits_by_status.assert_called_once()
    assert result == audits


def test_get_all_audited_documents():
    mock_audit_crud = Mock()
    mock_audit_crud.get_audits_by_status.return_value = audits
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.get_all_audited_documents()

    mock_audit_crud.get_audits_by_status.assert_called_once()
    assert result == audits


def test_get_all_audits_for_user():
    mock_audit_crud = Mock()
    mock_audit_crud.get_audits_by_user.return_value = audits
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.get_all_audits_for_user("username")

    mock_audit_crud.get_audits_by_user.assert_called_once()
    assert result == audits


def test_get_audit_by_document_id():
    mock_audit_crud = Mock()
    mock_audit_crud.get_audit_by_document_id.return_value = audits[0]
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        result = audit_service.get_audit_by_document_id(1)

    mock_audit_crud.get_audit_by_document_id.assert_called_once()
    assert result == audits[0]

def test_audit_document_not_found():
    mock_audit_crud = Mock()
    mock_audit_crud.get_audit_by_document_id.return_value = None
    db = Mock()

    audit_service = AuditService(db)

    with patch("app.services.audit.AuditCRUD", return_value=mock_audit_crud):
        with raises(AuditException.DocumentAuditNotFound):
            audit_service.audit_document(1)

    mock_audit_crud.get_audit_by_document_id.assert_called_once()

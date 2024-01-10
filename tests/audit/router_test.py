from unittest.mock import Mock, patch

from starlette.testclient import TestClient

from app.main import app
from app.services.audit import AuditService
from tests.audit.util import audits, audit_create

from tests.users.util import user_jwt, director_jwt, admin_jwt

client = TestClient(app)


def test_get_all_audits_not_authenticated():
    response = client.get("/audits/")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/audits/", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_all_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_audits.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_all_audits.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_usr_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_audits_for_user.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/?user_id=1", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_all_audits_for_user.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_pending_audits_for_usr():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_pending_audits.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/?user_id=1&status=pending", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_pending_audits.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_audited_audits_for_usr():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_audited_documents.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/?user_id=1&status=done", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_audited_documents.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_pending_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_pending_audits.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/?status=pending", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_all_pending_audits.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_audited_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_audited_documents.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/?status=done", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_all_audited_documents.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_my_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_audits_for_user_by_username.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/me", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_audit_service.get_all_audits_for_user_by_username.assert_called_once()
    mock_audit_service.get_all_audits_for_user.assert_not_called()

    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_my_pending_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_pending_audits_by_username.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/me?status=pending", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_audit_service.get_pending_audits_by_username.assert_called_once()
    mock_audit_service.get_pending_audits.assert_not_called()

    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_my_audited_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_audited_documents_by_username.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/me?status=done", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_audit_service.get_audited_documents_by_username.assert_called_once()
    mock_audit_service.get_audited_documents.assert_not_called()

    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_create_audit_request():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.create_audit_request.return_value = audits[0].model_dump()

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/create", headers={"Authorization": f"Bearer {admin_jwt}"}, json=audit_create.model_dump())

    mock_audit_service.create_audit_request.assert_called_once()
    assert response.status_code == 200
    assert response.json() == audits[0].model_dump()


def test_create_audit_request_not_authorized():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.create_audit_request.return_value = audits[0].model_dump()

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/create", headers={"Authorization": f"Bearer {user_jwt}"}, json=audit_create.model_dump())

    mock_audit_service.create_audit_request.assert_not_called()
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_audit_document():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.audit_document.return_value = audits[0].model_dump()

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/1", headers={"Authorization": f"Bearer {admin_jwt}"})

    mock_audit_service.audit_document.assert_called_once()
    assert response.status_code == 200
    assert response.json() == audits[0].model_dump()


def test_audit_document_not_authorized():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.audit_document.return_value = True

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/1", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_audit_service.audit_document.assert_not_called()
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}

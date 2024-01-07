import os
from unittest.mock import Mock, patch

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.services.audit import AuditService
from tests.audit.util import audits
from tests.users.util import user_jwt, director_jwt

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


def test_get_pending_audits_not_authenticated():
    response = client.get("/audits/pending")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/audits/pending", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_pending_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_pending_audits.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/pending", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_pending_audits.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_audited_documents_not_authenticated():

    response = client.get("/audits/audited")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/audits/audited", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_audited_documents():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_audited_documents.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/audited", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_audited_documents.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_create_audit_request_not_authenticated():
    response = client.post("/audits/create")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.post("/audits/create", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_create_audit_request():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.create_audit_request.return_value = audits[0].model_dump()

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/create", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.create_audit_request.assert_called_once()
    assert response.status_code == 200
    assert response.json() == audits[0].model_dump()


def test_get_all_pending_audits_not_authenticated():
    response = client.get("/audits/pending/all")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/audits/pending/all", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_all_pending_audits():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_pending_audits.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/pending/all", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_all_pending_audits.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_audited_documents_not_authenticated():
    response = client.get("/audits/audited/all")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/audits/audited/all", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_all_audited_documents():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_audited_documents.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/audited/all", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_all_audited_documents.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_all_audits_for_user_not_authenticated():
    response = client.get("/audits/all")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/audits/all", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_all_audits_for_user():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_all_audits_for_user.return_value = [audits[0].model_dump(), audits[1].model_dump()]

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/all", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_all_audits_for_user.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [audits[0].model_dump(), audits[1].model_dump()]


def test_get_audit_by_document_id_not_authenticated():

    response = client.get("/audits/1")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/audits/1", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_audit_by_document_id():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.get_audit_by_document_id.return_value = audits[0].model_dump()

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.get("/audits/1", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.get_audit_by_document_id.assert_called_once()
    assert response.status_code == 200
    assert response.json() == audits[0].model_dump()


def test_audit_document_not_authenticated():

    response = client.post("/audits/1/audit")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.post("/audits/1/audit", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_audit_document():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.audit_document.return_value = True

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/1/audit", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.audit_document.assert_called_once()
    assert response.status_code == 200
    assert response.json() == True


def test_audit_document_not_found():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.audit_document.side_effect = Exception

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/1/audit", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.audit_document.assert_called_once()
    assert response.status_code == 500
    assert response.json() == {'app_exception': 'Exception', 'context': {}}


def test_audit_document_already_audited():
    mock_audit_service = Mock(spec=AuditService)
    mock_audit_service.audit_document.side_effect = Exception

    with patch("app.routers.audit.AuditService", return_value=mock_audit_service):
        response = client.post("/audits/1/audit", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_audit_service.audit_document.assert_called_once()
    assert response.status_code == 500
    assert response.json() == {'app_exception': 'Exception', 'context': {}}

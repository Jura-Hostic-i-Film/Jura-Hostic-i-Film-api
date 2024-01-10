import os
from unittest.mock import Mock, patch

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.services.documents import DocumentService
from tests.documents.util import documents, imageDB
from tests.users.util import user_jwt, director_jwt

client = TestClient(app)


def test_get_all_documents_not_approved():
    response = client.get("/documents/")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/documents/", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': "NotAuthorized", 'context': {}}


def test_get_all_documents():
    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.get_all_documents.return_value = [documents[0].model_dump(), documents[1].model_dump()]

    with patch("app.routers.documents.DocumentService", return_value=mock_document_service):
        response = client.get("/documents/", headers={"Authorization": f"Bearer {director_jwt}"})

    mock_document_service.get_all_documents.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [documents[0].model_dump(), documents[1].model_dump()]


def test_get_me_not_authenticated():
    response = client.get("/documents/me")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}


def test_get_me():
    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.get_documents.return_value = [documents[0].model_dump(), documents[1].model_dump()]

    with patch("app.routers.documents.DocumentService", return_value=mock_document_service):
        response = client.get("/documents/me", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_document_service.get_documents.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [documents[0].model_dump(), documents[1].model_dump()]


def test_create_document():
    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.create_document.return_value = documents[0].model_dump()

    file_path = os.path.join(os.path.dirname(__file__), 'files', 'test_image.png')
    if os.path.isfile(file_path):
        _files = {'image': open(file_path, 'rb')}
        with patch("app.routers.documents.DocumentService", return_value=mock_document_service):
            response = client.post('/documents/create', headers={"Authorization": f"Bearer {user_jwt}"},
                                   files=_files)
        assert response.status_code == 200
        assert response.json() == documents[0].model_dump()
    else:
        pytest.fail("Scratch file does not exists.")


def test_get_document():
    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.get_document.return_value = documents[0].model_dump()

    with patch("app.routers.documents.DocumentService", return_value=mock_document_service):
        response = client.get("/documents/document/1", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_document_service.get_document.assert_called_once()
    assert response.status_code == 200
    assert response.json() == documents[0].model_dump()


def test_get_image():
    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.get_image.return_value = imageDB

    with patch("app.routers.documents.DocumentService", return_value=mock_document_service):
        response = client.get("/documents/image/1", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_document_service.get_image.assert_called_once()
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'
    assert response.iter_bytes()


def test_update_document():
    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.update_document.return_value = documents[0].model_dump()

    with patch("app.routers.documents.DocumentService", return_value=mock_document_service):
        response = client.post("/documents/update/1", headers={"Authorization": f"Bearer {user_jwt}"},
                               params={'new_status': 'approved'})

    mock_document_service.update_document.assert_called_once()
    assert response.status_code == 200
    assert response.json() == documents[0].model_dump()

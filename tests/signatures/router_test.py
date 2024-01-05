from unittest.mock import Mock, patch
from app.main import app
from starlette.testclient import TestClient
from _pytest.python_api import raises
from app.services.signatures import SignatureService
from tests.signatures.util import signatures, signature_create
from tests.users.util import user_jwt, director_jwt
from pydantic import BaseModel

client = TestClient(app)


def test_get_all_signatures_not_approved():
    response = client.get("/signatures/")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/signatures/", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': 'NotAuthorized', 'context': {}}


def test_sign_document():
    mock_signature_service = Mock(spec=SignatureService)
    mock_signature_service.sign_document.return_value = True

    with patch("app.routers.signatures.SignatureService", return_value=mock_signature_service):
        response = client.post("/signatures/signature/1", headers={"Authorization": f"Bearer {user_jwt}"})

    mock_signature_service.sign_document.assert_called_once_with(1)
    assert response.status_code == 200
    assert response.json() == True


def test_get_me_not_authenticated():
    response = client.get("/signatures/me")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

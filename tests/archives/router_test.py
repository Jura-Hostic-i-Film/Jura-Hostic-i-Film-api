from unittest.mock import Mock, patch
from app.main import app
from starlette.testclient import TestClient
from app.services.archives import ArchiveService
from tests.archives.util import archive1
from tests.users.util import user_jwt

client = TestClient(app)


def test_get_all_archives_not_authorized_and_authenticated():
    response = client.get("/archives/")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

    response = client.get("/archives/", headers={"Authorization": f"Bearer {user_jwt}"})
    assert response.status_code == 403
    assert response.json() == {'app_exception': 'NotAuthorized', 'context': {}}


def test_get_me_not_authenticated():
    response = client.get("/archives/me")
    assert response.status_code == 401
    assert response.json() == {'app_exception': 'NotAuthenticated', 'context': {}}

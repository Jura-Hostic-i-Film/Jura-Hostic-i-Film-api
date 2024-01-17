from unittest.mock import Mock, patch

from _pytest.python_api import raises

from app.services.documents import DocumentService
from app.services.users import UserService
from app.utils.enums import ActionStatus, ArchiveStatus
from app.services.archives import ArchiveService
from app.utils.exceptions.archive_exceptions import ArchiveException
from tests.archives.util import archive1, archive2, archives, archive_create, archive3
from tests.users.util import admin


def test_get_all_archives():
    mock_archive_crud = Mock()
    mock_archive_crud.get_all_archives.return_value = archives
    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        result = archive_service.get_all_archives()

    mock_archive_crud.get_all_archives.assert_called_once()
    assert result == archives


def test_get_all_pending_archives():
    mock_archive_crud = Mock()
    mock_archive_crud.get_archives_by_status.return_value = archives
    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        result = archive_service.get_archives_by_status(ArchiveStatus.PENDING)

    mock_archive_crud.get_archives_by_status.assert_called_once_with(ActionStatus.PENDING)
    assert result == archives


def test_archive_document():
    mock_archive_crud = Mock()
    mock_archive_crud.get_archived_by_document_id.return_value = archive1
    mock_archive_crud.update_archive.return_value = archive1

    mock_user_service = Mock(spec=UserService)
    mock_user_service.get_user.return_value = admin

    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.update_document.return_value = None

    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        with patch("app.services.archives.UserService", return_value=mock_user_service):
            with patch("app.services.archives.DocumentService", return_value=mock_document_service):
                result = archive_service.archive_document(1, ArchiveStatus.DONE, "test")

    mock_archive_crud.get_archived_by_document_id.assert_called_once_with(1)
    mock_archive_crud.update_archive.assert_called_once()
    assert result == archive1


def test_archive_document_forbidden():
    mock_archive_crud = Mock()
    mock_archive_crud.get_archived_by_document_id.return_value = archive3
    mock_archive_crud.update_archive.return_value = archive1

    mock_user_service = Mock(spec=UserService)
    mock_user_service.get_user.return_value = admin

    mock_document_service = Mock(spec=DocumentService)
    mock_document_service.update_document.return_value = None

    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        with patch("app.services.archives.UserService", return_value=mock_user_service):
            with patch("app.services.archives.DocumentService", return_value=mock_document_service):
                with raises(ArchiveException.IllegalArchiveStatus):
                    archive_service.archive_document(1, ArchiveStatus.DONE, "test")


def test_create_archive():
    mock_archive_crud = Mock()
    mock_archive_crud.create_archive.return_value = archive1
    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        result = archive_service.create_archive_request(archive_create)

    mock_archive_crud.create_archive.assert_called_once_with(archive_create)
    assert result == archive1

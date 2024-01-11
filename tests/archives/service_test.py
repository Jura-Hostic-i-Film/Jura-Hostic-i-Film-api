from unittest.mock import Mock, patch
from app.utils.enums import ActionStatus
from app.services.archives import ArchiveService
from tests.archives.util import archive1, archive2, archives, archive_create
from _pytest.python_api import raises
from pydantic import BaseModel


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
        result = archive_service.get_all_pending_archives()

    mock_archive_crud.get_archives_by_status.assert_called_once_with(ActionStatus.PENDING)
    assert result == archives


def test_get_all_archived_documents():
    mock_archive_crud = Mock()
    mock_archive_crud.get_archives_by_status.return_value = archives
    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        result = archive_service.get_all_archived_documents()

    mock_archive_crud.get_archives_by_status.assert_called_once_with(ActionStatus.DONE)
    assert result == archives


def test_archive_document():
    mock_archive_crud = Mock()
    mock_archive_crud.get_archived_by_document_id.return_value = archive1
    mock_archive_crud.update_archive.return_value = archive1
    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        result = archive_service.archive_document(1)

    mock_archive_crud.get_archived_by_document_id.assert_called_once_with(1)
    mock_archive_crud.update_archive.assert_called_once()
    assert result == archive1


def test_create_archive():
    mock_archive_crud = Mock()
    mock_archive_crud.create_archive.return_value = archive1
    db = Mock()

    archive_service = ArchiveService(db)

    with patch("app.services.archives.ArchiveCRUD", return_value=mock_archive_crud):
        result = archive_service.create_archive_request(archive_create)

    mock_archive_crud.create_archive.assert_called_once_with(archive_create)
    assert result == archive1

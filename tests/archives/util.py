from datetime import datetime
from app.models.archives import ArchiveDB
from app.schemas.archives import ArchiveCreate
from app.utils.enums import ActionStatus
from tests.users.util import admin, director

archive1 = ArchiveDB(
    archive_number=1,
    status=ActionStatus.PENDING,
    archive_at=datetime.now(),
    document_id=1,
    archive_by=admin.id,
)

archive2 = ArchiveDB(
    archive_number=2,
    status=ActionStatus.DONE,
    archive_at=datetime.now(),
    document_id=2,
    archive_by=director.id,
)

archives = [archive1, archive2]

archive_create = ArchiveCreate(
    document_id=1,
    archive_by=director.id,
)

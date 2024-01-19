from datetime import datetime
from app.models.archives import ArchiveDB
from app.schemas.archives import ArchiveCreate
from app.utils.enums import ArchiveStatus
from tests.users.util import admin, director

archive1 = ArchiveDB(
    archive_number=1,
    status=ArchiveStatus.PENDING,
    archive_at=datetime.now(),
    document_id=1,
    archive_by=2,
)

archive2 = ArchiveDB(
    archive_number=2,
    status=ArchiveStatus.DONE,
    archive_at=datetime.now(),
    document_id=2,
    archive_by=director.id,
)

archive3 = ArchiveDB(
    archive_number=3,
    status=ArchiveStatus.AWAITING_SIGNATURE,
    archive_at=None,
    document_id=1,
    archive_by=2,
)

archives = [archive1, archive2]

archive_create = ArchiveCreate(
    document_id=1,
    archive_by=director.id,
)

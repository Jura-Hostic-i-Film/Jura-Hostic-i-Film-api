from pydantic import BaseModel
from datetime import datetime

from app.utils.enums import ArchiveStatus
from app.schemas.users import User
from app.schemas.documents import Document


class Archive(BaseModel):
    document: Document
    archived: User
    archive_number: int
    status: ArchiveStatus
    archive_at: datetime | None = None

    class Config:
        from_attributes = True
        use_enum_values = True

    def __dict__(self):
        return {"document": self.document,
                "archive_by": self.archive_by,
                "archive_number": self.archive_number,
                "status": self.status,
                "archive_at": self.archived_at}


class ArchiveCreate(BaseModel):
    document_id: int
    archive_by: int

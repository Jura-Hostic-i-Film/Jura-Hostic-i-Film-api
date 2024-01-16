from pydantic import BaseModel, field_serializer
from datetime import datetime

from app.utils.enums import ActionStatus
from app.schemas.users import User
from app.schemas.documents import Document


class Audit(BaseModel):
    audit_id: int
    status: ActionStatus
    audited_at: datetime | None = None
    audited: User
    document: Document

    @field_serializer('audited_at')
    def serialize_dt(self, audited_at: datetime | None, _info):
        return audited_at.strftime('%Y-%m-%dT%H:%M:%SZ') if audited_at else None

    class Config:
        from_attributes = True
        use_enum_values = True

    def __dict__(self):
        return {"audit_id": self.audit_id,
                "audit_status": self.audit_status,
                "audited_at": self.audited_at,
                "audited_by": self.audited_by,
                "document": self.document}


class AuditCreate(BaseModel):
    audit_by: int
    document_id: int


class DocumentSummary(BaseModel):
    summary: str

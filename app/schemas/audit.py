from pydantic import BaseModel
from datetime import datetime

from app.utils.enums import ActionStatus
from app.schemas.users import User
from app.schemas.documents import Document

class Audit(BaseModel):
    audit_id: int
    audit_status: ActionStatus
    audited_at: datetime
    audited_by: User
    document: Document

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
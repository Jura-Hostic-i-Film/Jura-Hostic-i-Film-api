from datetime import datetime

from pydantic import BaseModel


from app.utils.enums import ActionStatus
from app.schemas.users import User
from app.schemas.documents import Document


class Signature(BaseModel):
    document: Document
    sign_by: User
    signature_id: int
    signature_status: ActionStatus
    signed_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __dict__(self):
        return {"document": self.document,
                "sign_by": self.sign_by,
                "signature_id": self.signature_id,
                "signature_status": self.signature_status,
                "signed_at": self.signed_at}


class SignatureCreate(BaseModel):
    document_id: int
    sign_by: int

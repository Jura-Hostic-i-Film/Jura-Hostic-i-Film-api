from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel, field_serializer

from app.schemas.users import User
from app.utils.enums import DocumentTypeEnum, DocumentStatusEnum


class Image(BaseModel):
    id: int
    image_file: UploadFile

    class Config:
        from_attributes = True


class Document(BaseModel):
    id: int
    image_id: int
    owner: User
    document_type: DocumentTypeEnum
    summary: str
    document_status: DocumentStatusEnum
    scan_time: datetime

    @field_serializer('scan_time')
    def serialize_dt(self, scan_time: datetime, _info):
        return scan_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    class Config:
        from_attributes = True
        use_enum_values = True

    def __dict__(self):
        return {'id': self.id,
                'image_id': self.image_id,
                'owner': self.owner,
                'document_type': self.document_type.name,
                'summary': self.summary,
                'document_status': self.document_status.name,
                'scan_time': self.scan_time}

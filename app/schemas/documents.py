from datetime import datetime
from pydantic import BaseModel

from app.utils.enums import DocumentTypeEnum, DocumentStatusEnum


class DocumentCreate(BaseModel):
    image_file: bytes  # TODO help
    scan_time: datetime


class Document(BaseModel):
    id: int
    image_id: int
    owner_id: int  # like this?
    document_type: DocumentTypeEnum
    summary: str
    document_status: DocumentStatusEnum
    scan_time: datetime

    class Config:
        from_attributes = True


class Image(BaseModel):
    id: int
    image_file: bytes
    document: Document  # ok?

from typing import BinaryIO

from fastapi import UploadFile

from app.models.documents import ImageDB
from app.schemas.documents import Document, Image
from app.utils.enums import DocumentTypeEnum, DocumentStatusEnum
from tests.users.util import admin, director


image_file = BinaryIO()
uploaded_image = UploadFile(
    filename="test_image",
    file=image_file,
)
image = Image(
    id=1,
    image_file=uploaded_image
)
imageDB = ImageDB(
    id=1,
    image_file=uploaded_image.file.read(),
)
document1 = Document(
    id=1,
    image_id=1,
    owner=admin,
    document_type=DocumentTypeEnum.OFFER,
    summary="test",
    document_status=DocumentStatusEnum.SCANNED,
    scan_time="2021-01-01T00:00:00",
)
document2 = Document(
    id=2,
    image_id=1,
    owner=director,
    document_type=DocumentTypeEnum.INTERNAL,
    summary="test",
    document_status=DocumentStatusEnum.APPROVED,
    scan_time="2021-01-01T00:00:00",
)
documents = [document1, document2]

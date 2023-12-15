from random import randint
from typing import Type

from app.models.documents import DocumentDB, ImageDB
from app.schemas.documents import DocumentCreate, Document, Image
from app.services.main import AppService, AppCRUD
from app.services.users import UserService
from app.utils.enums import DocumentTypeEnum, DocumentStatusEnum
from app.utils.exceptions.document_exceptions import DocumentException


class DocumentService(AppService):
    def get_all_documents(self, document_type: str, document_status: str) -> list[Type[DocumentDB]]:
        documents = DocumentCRUD(self.db).get_all_documents(document_type, document_status)
        return documents

    def get_documents(self, owner_username: str) -> list[Type[DocumentDB]]:
        owner = UserService(self.db).get_user(owner_username)
        documents = DocumentCRUD(self.db).get_documents(owner.id)
        return documents

    def create_document(self, document: DocumentCreate, owner_username: str) -> Document:
        owner = UserService(self.db).get_user(owner_username)
        document_status = DocumentStatusEnum.SCANNED
        summary = "Summary"   # give me OCR here?
        rand = randint(1, 3)  # because why not
        if rand == 1:
            document_type = DocumentTypeEnum.OFFER
        elif rand == 2:
            document_type = DocumentTypeEnum.RECEIPT
        else:
            document_type = DocumentTypeEnum.INTERNAL

        document = DocumentCRUD(self.db).create_document(document, owner.id, document_type, summary, document_status)
        return document

    def get_document(self, document_id: int) -> Document:
        document = DocumentCRUD(self.db).get_document(document_id)
        if not document:
            raise DocumentException.DocumentNotFound({"document_id": document_id})
        return document

    def get_image(self, document_id: int) -> bytes:
        document = self.get_document(document_id)
        image = DocumentCRUD(self.db).get_image(document.image_id)
        return image.image_file

    def update_document(self, document_id: int, new_status: DocumentStatusEnum) -> Document:
        document = self.get_document(document_id)
        document = DocumentCRUD(self.db).update_document(document, new_status)
        return document


class DocumentCRUD(AppCRUD):
    def create_document(self, document: DocumentCreate, owner_id: int, document_type: DocumentTypeEnum, summary: str,
                        document_status: DocumentStatusEnum) -> Document:
        image = self.create_image(document.image_file)
        documentdb = DocumentDB(
            image_id=image.id,
            owner_id=owner_id,
            document_type=document_type,
            summary=summary,
            document_status=document_status,
            scan_time=document.scan_time
        )
        self.db.add(documentdb)
        self.db.commit()
        self.db.refresh(documentdb)
        return documentdb

    def create_image(self, image_file: bytes) -> Image:
        imagedb = ImageDB(
            image_file=image_file
        )
        self.db.add(imagedb)
        self.db.commit()
        self.db.refresh(imagedb)
        return imagedb

    def get_documents(self, owner_id: int) -> list[Type[DocumentDB]]:
        return self.db.query(DocumentDB).filter(DocumentDB.owner_id == owner_id).all()

    def get_all_documents(self, document_type: str, document_status: str) -> list[Type[DocumentDB]]:
        if document_type is not None and document_status is not None:
            return (self.db.query(DocumentDB).
                    filter(DocumentDB.document_type == document_type, DocumentDB.document_status == document_status).
                    all())
        elif document_type is not None:
            return self.db.query(DocumentDB).filter(DocumentDB.document_type == document_type).all()
        elif document_status is not None:
            return self.db.query(DocumentDB).filter(DocumentDB.document_status == document_status).all()
        else:
            return self.db.query(DocumentDB).all()

    def get_document(self, document_id: int) -> Type[DocumentDB]:
        return self.db.query(DocumentDB).filter(DocumentDB.id == document_id).first()

    def get_image(self, image_id: int) -> Type[ImageDB]:
        return self.db.query(ImageDB).filter(ImageDB.id == image_id).first()

    def update_document(self, document: Document, new_status: DocumentStatusEnum) -> Document:
        document.document_status = new_status  # don't know if this line here or in the service
        self.db.commit()
        self.db.refresh(document)
        return document

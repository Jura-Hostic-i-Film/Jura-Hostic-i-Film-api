import os
from datetime import datetime
from random import randint
from typing import Type

from fastapi import UploadFile, File

from app.config.base import settings
from app.config.database import IMAGE_STORAGE_CONNECTION_STRING
from app.models.documents import DocumentDB, ImageDB
from app.schemas.documents import Document
from app.services.main import AppService, AppCRUD
from app.services.users import UserService
from app.utils.enums import DocumentTypeEnum, DocumentStatusEnum
from app.utils.exceptions.document_exceptions import DocumentException

import app.services.audit as audit
from app.utils.util import COMPATIBLE_STATUSES


class DocumentService(AppService):
    def get_all_documents(self, document_type: str, document_status: str) -> list[Type[DocumentDB]]:
        documents = DocumentCRUD(self.db).get_all_documents(document_type, document_status)
        return documents

    def get_documents(self, owner_username: str) -> list[Type[DocumentDB]]:
        owner = UserService(self.db).get_user(owner_username)
        return self.get_documents_by_user_id(owner.id)

    def get_documents_by_user_id(self, owner_id: int) -> list[Type[DocumentDB]]:
        documents = DocumentCRUD(self.db).get_documents(owner_id)
        return documents

    def create_document(self, image: UploadFile, owner_username: str) -> Document:
        owner = UserService(self.db).get_user(owner_username)
        document_status = DocumentStatusEnum.SCANNED
        summary = "Summary"  # give me OCR here?
        rand = randint(1, 3)  # because why not
        if rand == 1:
            document_type = DocumentTypeEnum.OFFER
        elif rand == 2:
            document_type = DocumentTypeEnum.RECEIPT
        else:
            document_type = DocumentTypeEnum.INTERNAL

        image_db = ImageCRUD(self.db).create_image(image)

        document = DocumentCRUD(self.db).create_document(image_db, owner.id, document_type, summary, document_status)
        return document

    def get_document(self, document_id: int) -> Document:
        document = DocumentCRUD(self.db).get_document(document_id)
        if not document:
            raise DocumentException.DocumentNotFound({"document_id": document_id})
        return document

    def update_document(self, document_id: int, new_status: DocumentStatusEnum) -> Document:
        if new_status is None:
            raise DocumentException.DocumentStatusNotProvided()

        document = self.get_document(document_id)

        if not document:
            raise DocumentException.DocumentNotFound({"document_id": document_id})

        if new_status not in COMPATIBLE_STATUSES[document.document_status]:
            raise DocumentException.DocumentStatusNotCompatible({"document_status": document.document_status,
                                                                 "new_status": new_status})

        document.document_status = new_status
        document = DocumentCRUD(self.db).update_document(document)
        return document

    def approve_document(self, document_id: int) -> Document:
        document = self.update_document(document_id, DocumentStatusEnum.APPROVED)

        audit.AuditService(self.db).create_audit_for_document(document_id)

        return document


class DocumentCRUD(AppCRUD):
    def create_document(self, image: ImageDB, owner_id: int, document_type: DocumentTypeEnum, summary: str,
                        document_status: DocumentStatusEnum) -> Document:
        documentdb = DocumentDB(
            image_id=image.id,
            owner_id=owner_id,
            document_type=document_type,
            summary=summary,
            document_status=document_status,
            scan_time=datetime.now()
        )
        self.db.add(documentdb)
        self.db.commit()
        self.db.refresh(documentdb)
        return documentdb

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

    def update_document(self, document: Document) -> Document:
        self.db.commit()
        self.db.refresh(document)
        return document


class ImageService(AppService):
    def get_image(self, image_id: int) -> UploadFile:
        image = ImageCRUD(self.db).get_image(image_id)
        return image

    def create_image(self, image_file: UploadFile) -> ImageDB:
        image = ImageCRUD(self.db).create_image(image_file)
        return image


class ImageCRUD(AppCRUD):
    IMAGE_PATH = settings.image_path
    IMAGE_CONNECTION_STRING = IMAGE_STORAGE_CONNECTION_STRING if "None" not in IMAGE_STORAGE_CONNECTION_STRING else None

    def __init__(self, db):
        super().__init__(db)
        if self.IMAGE_CONNECTION_STRING:
            from azure.storage.blob import BlobServiceClient
            self.blob_service_client = BlobServiceClient.from_connection_string(self.IMAGE_CONNECTION_STRING)
            self.container_client = self.blob_service_client.get_container_client(self.IMAGE_PATH)

    def get_image(self, image_id: int) -> UploadFile:
        image_path = self.db.query(ImageDB).filter(ImageDB.id == image_id).first().image_path

        if self.IMAGE_CONNECTION_STRING:
            # get image from blob storage
            try:
                image_data = self.container_client.download_blob(image_path)
                image_file = UploadFile(filename=image_path, file=image_data.readall())
            except FileNotFoundError:
                raise DocumentException.ImageNotFound({"image_id": image_id})
        else:
            # get image from disk
            try:
                image_file = open(image_path, "rb")
            except FileNotFoundError:
                raise DocumentException.ImageNotFound({"image_id": image_id})

        return image_file

    def create_image(self, image_file: UploadFile) -> ImageDB:
        image_path_split = image_file.filename.split(".")
        image_name = ".".join(image_path_split[:-1])
        image_extension = image_path_split[-1]

        if self.IMAGE_CONNECTION_STRING:
            # upload image to blob storage
            image_path = f"{image_name}"
            blob = self.container_client.get_blob_client(image_path)

            while blob.exists():
                image_path = f"{image_name}_{randint(0, 1000000)}"
                blob = self.container_client.get_blob_client(image_path)

            blob.upload_blob(image_file.file.read())

        else:
            # save image to disk
            image_path = f"{self.IMAGE_PATH}/{image_file.filename}"

            while os.path.exists(image_path):
                image_path = f"{self.IMAGE_PATH}/{image_name}_{randint(0, 1000000)}.{image_extension}"

            with open(image_path, "wb") as buffer:
                buffer.write(image_file.file.read())

        image_db = ImageDB(
            image_path=image_path,
        )

        self.db.add(image_db)
        self.db.commit()
        self.db.refresh(image_db)

        return image_db

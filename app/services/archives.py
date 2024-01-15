from app.models.archives import ArchiveDB
from app.schemas.archives import Archive, ArchiveCreate
from app.services.main import AppService
from typing import Type
from datetime import datetime

from app.services.users import UserService
from app.utils.enums import DocumentTypeEnum, RolesEnum, ArchiveStatus
from app.utils.exceptions.archive_exceptions import ArchiveException
from app.utils.exceptions.user_exceptions import UserException

import app.services.signatures as signatures


class ArchiveCRUD(AppService):
    def get_all_archives(self) -> list[Type[ArchiveDB]]:
        return self.db.query(ArchiveDB).all()

    def get_archives_by_status(self, status: ArchiveStatus) -> list[Type[ArchiveDB]]:
        return self.db.query(ArchiveDB).filter(status == ArchiveDB.status).all()

    def get_archives_by_user(self, user_id: int) -> list[Type[ArchiveDB]]:
        return self.db.query(ArchiveDB).filter(user_id == ArchiveDB.archive_by).all()

    def get_archives_by_user_and_status(self, user_id: int, status: ArchiveStatus) -> list[Type[ArchiveDB]]:
        return self.db.query(ArchiveDB).filter(user_id == ArchiveDB.archive_by, status == ArchiveDB.status).all()

    def create_archive(self, archive: ArchiveCreate) -> ArchiveDB:
        archive_db = self.db.query(ArchiveDB).filter(ArchiveDB.document_id == archive.document_id).first()
        if archive_db:
            raise ArchiveException.DocumentArchiveAlreadyExists({"document_id": archive.document_id})

        archiveDB = ArchiveDB(
            status=ArchiveStatus.PENDING,
            archive_by=archive.archive_by,
            document_id=archive.document_id
        )

        self.db.add(archiveDB)
        self.db.commit()
        self.db.refresh(archiveDB)
        return archiveDB

    def get_archived_by_document_id(self, document_id: int) -> ArchiveDB:
        return self.db.query(ArchiveDB).filter(document_id == ArchiveDB.document_id).first()

    def update_archive(self, archive: ArchiveDB) -> ArchiveDB:
        self.db.commit()
        self.db.refresh(archive)
        return archive


class ArchiveService(AppService):
    def get_all_archives(self) -> list[Type[ArchiveDB]]:
        return ArchiveCRUD(self.db).get_all_archives()

    def get_archives_by_status(self, status: ArchiveStatus) -> list[Type[ArchiveDB]]:
        return ArchiveCRUD(self.db).get_archives_by_status(status)

    def get_archives_by_user_and_status(self, user_id: int, status: ArchiveStatus) -> list[Type[ArchiveDB]]:
        return ArchiveCRUD(self.db).get_archives_by_user_and_status(user_id, status)

    def get_all_archives_for_user_by_id(self, user_id: int) -> list[Type[ArchiveDB]]:
        return ArchiveCRUD(self.db).get_archives_by_user(user_id)

    def get_all_archives_for_user_by_username(self, username: str) -> list[Type[ArchiveDB]]:
        user = UserService(self.db).get_user(username)

        if not user:
            raise UserException.UserNotFound({"username": username})

        user_id = user.id
        return ArchiveCRUD(self.db).get_archives_by_user(user_id)

    def get_pending_archives_by_username(self, username: str) -> list[Type[ArchiveDB]]:
        user = UserService(self.db).get_user(username)

        if not user:
            raise UserException.UserNotFound({"username": username})

        user_id = user.id
        # returns both pending and signed_pending
        return (ArchiveCRUD(self.db).get_archives_by_user_and_status(user_id, ArchiveStatus.PENDING)
                + ArchiveCRUD(self.db).get_archives_by_user_and_status(user_id, ArchiveStatus.SIGNED_PENDING))

    def get_archives_awaiting_signature_by_username(self, username: str) -> list[Type[ArchiveDB]]:
        user = UserService(self.db).get_user(username)

        if not user:
            raise UserException.UserNotFound({"username": username})

        user_id = user.id
        return ArchiveCRUD(self.db).get_archives_by_user_and_status(user_id, ArchiveStatus.AWAITING_SIGNATURE)

    def get_archived_documents_by_username(self, username: str) -> list[Type[ArchiveDB]]:
        user = UserService(self.db).get_user(username)

        if not user:
            raise UserException.UserNotFound({"username": username})

        user_id = user.id
        return ArchiveCRUD(self.db).get_archives_by_user_and_status(user_id, ArchiveStatus.DONE)

    def get_archive_status(self, document_id: int) -> ArchiveStatus:
        archive = ArchiveCRUD(self.db).get_archived_by_document_id(document_id)
        if not archive:
            raise ArchiveException.DocumentArchiveNotFound({"document_id": document_id})
        return ArchiveStatus(archive.status)

    def create_archive_request(self, archive_request: ArchiveCreate) -> ArchiveDB:
        return ArchiveCRUD(self.db).create_archive(archive_request)

    def get_archive_by_document_id(self, document_id: int) -> Archive:
        archive = ArchiveCRUD(self.db).get_archived_by_document_id(document_id)
        if not archive:
            raise ArchiveException.DocumentArchiveNotFound({"document_id": document_id})
        return archive

    def archive_document(self, document_id: int, status: ArchiveStatus, username: str) -> Archive:
        archive = ArchiveCRUD(self.db).get_archived_by_document_id(document_id)
        if not archive:
            raise ArchiveException.DocumentArchiveNotFound({"document_id": document_id})

        accountant = UserService(self.db).get_user(username)
        if not accountant:
            raise UserException.UserNotFound({"username": username})
        if accountant.id != archive.archive_by:
            raise UserException.UserNotAuthorized({"username": username})

        if status == ArchiveStatus.DONE:
            if archive.status != ArchiveStatus.PENDING and archive.status != ArchiveStatus.SIGNED_PENDING:
                raise ArchiveException.IllegalArchiveStatus({"status": archive.status})
            archive.archive_at = datetime.now()
        elif status == ArchiveStatus.AWAITING_SIGNATURE:
            if archive.status != ArchiveStatus.PENDING:
                raise ArchiveException.IllegalArchiveStatus({"status": archive.status})
            signatures.SignatureService(self.db).create_signature_for_document(document_id)
        else:
            raise ArchiveException.IllegalArchiveStatus({"status": status})

        archive.status = status
        archive = ArchiveCRUD(self.db).update_archive(archive)
        return archive

    def create_archive_for_document(self, document_id: int, document_type: DocumentTypeEnum) -> ArchiveDB:
        if document_type == DocumentTypeEnum.INTERNAL:
            accountant_type = RolesEnum.ACCOUNTANT_INTERNAL
        elif document_type == DocumentTypeEnum.OFFER:
            accountant_type = RolesEnum.ACCOUNTANT_OFFER
        elif document_type == DocumentTypeEnum.RECEIPT:
            accountant_type = RolesEnum.ACCOUNTANT_RECEIPT
        else:
            raise ArchiveException.DocumentTypeNotProvided({"document_type": document_type})

        accountants = UserService(self.db).get_users([accountant_type])

        if not accountants:
            raise UserException.NoUsersWithRole({"role": accountant_type})

        # Find accountant with the least amount of pending archives
        accountants_with_pending_archives = []

        for accountant in accountants:
            pending_archives = (self.get_archives_by_user_and_status(accountant.id, ArchiveStatus.PENDING)
                                + self.get_archives_by_user_and_status(accountant.id, ArchiveStatus.SIGNED_PENDING))
            if pending_archives:
                accountants_with_pending_archives.append((accountant, len(pending_archives)))
            else:
                accountants_with_pending_archives.append((accountant, 0))

        accountant = min(accountants_with_pending_archives, key=lambda x: x[1])[0]

        archiveCreate = ArchiveCreate(
            document_id=document_id,
            archive_by=accountant.id
        )

        return self.create_archive_request(archiveCreate)

    def update_archive_request_after_signing(self, document_id: int) -> ArchiveDB:
        archive = ArchiveCRUD(self.db).get_archived_by_document_id(document_id)
        if not archive:
            raise ArchiveException.DocumentArchiveNotFound({"document_id": document_id})

        if archive.status != ArchiveStatus.AWAITING_SIGNATURE:
            raise ArchiveException.IllegalArchiveStatus({"status": archive.status})

        archive.status = ArchiveStatus.SIGNED_PENDING
        archive = ArchiveCRUD(self.db).update_archive(archive)
        return archive


from typing import Type

from app.models.audit import AuditDB
from app.schemas.audit import AuditCreate
from app.services.archives import ArchiveService
from app.services.main import AppService
from app.services.users import UserCRUD, UserService
from app.utils.enums import ActionStatus, DocumentStatusEnum, RolesEnum
from app.utils.exceptions.audit_exceptions import AuditException
from datetime import datetime

import app.services.documents as documents

from app.utils.exceptions.user_exceptions import UserException


class AuditService(AppService):
    def get_all_audits(self) -> list[Type[AuditDB]]:
        audits = AuditCRUD(self.db).get_all_audits()

        return audits

    def get_pending_audits(self, user_id: int) -> list[Type[AuditDB]]:
        audits = AuditCRUD(self.db).get_audits_by_user_and_status(user_id, ActionStatus.PENDING)

        return audits

    def get_audited_documents(self, user_id: int) -> list[Type[AuditDB]]:
        audits = AuditCRUD(self.db).get_audits_by_user_and_status(user_id, ActionStatus.DONE)

        return audits

    def create_audit_request(self, audit: AuditCreate) -> AuditDB:
        user = UserService(self.db).get_user_by_id(audit.audit_by)

        if not user:
            raise UserException.UserNotFound({"user_id": audit.audit_by})

        roles = [RolesEnum(role.name) for role in user.roles]

        if RolesEnum.AUDITOR not in roles:
            raise UserException.UserNotAuthorized({"user_id": audit.audit_by})

        audit_db = AuditCRUD(self.db).create_audit(audit)

        return audit_db

    def get_all_pending_audits(self) -> list[Type[AuditDB]]:
        audits = AuditCRUD(self.db).get_audits_by_status(ActionStatus.PENDING)

        return audits

    def get_all_audited_documents(self) -> list[Type[AuditDB]]:
        audits = AuditCRUD(self.db).get_audits_by_status(ActionStatus.DONE)

        return audits

    def get_all_audits_for_user(self, user_id: int) -> list[Type[AuditDB]]:
        audits = AuditCRUD(self.db).get_audits_by_user(user_id)

        return audits

    def get_audit_by_document_id(self, document_id: int) -> AuditDB:
        audit = AuditCRUD(self.db).get_audit_by_document_id(document_id)

        if not audit:
            raise AuditException.DocumentAuditNotFound({"document_id": document_id})

        return audit

    def audit_document(self, document_id: int, username: str) -> AuditDB:
        audit = AuditCRUD(self.db).get_audit_by_document_id(document_id)
        document = documents.DocumentService(self.db).get_document(document_id)
        user = UserService(self.db).get_user_by_id(audit.audited_by)

        if not user:
            raise UserException.UserNotFound({"user_id": audit.audited_by})

        if user.username != username:
            raise UserException.UserNotAuthorized({"username": username})

        if not audit:
            raise AuditException.DocumentAuditNotFound({"document_id": document_id})

        if audit.status == ActionStatus.DONE:
            raise AuditException.DocumentAlreadyAudited({"document_id": document_id})

        audit.status = ActionStatus.DONE
        audit.audited_at = datetime.now()

        AuditCRUD(self.db).update_audit(audit)

        documents.DocumentService(self.db).update_document(document_id, DocumentStatusEnum.AUDITED)

        # create an archive request for the document
        ArchiveService(self.db).create_archive_for_document(document_id, document.document_type)

        return audit

    def create_audit_for_document(self, document_id: int) -> AuditDB:
        auditors = UserService(self.db).get_users([RolesEnum.AUDITOR])

        if not auditors:
            raise UserException.NoUsersWithRole({"role": RolesEnum.AUDITOR})

        auditors_with_pending_audits = []

        for auditor in auditors:
            pending_audits = self.get_pending_audits(auditor.id)
            if pending_audits:
                auditors_with_pending_audits.append((auditor, len(pending_audits)))
            else:
                auditors_with_pending_audits.append((auditor, 0))

        auditor = min(auditors_with_pending_audits, key=lambda x: x[1])[0]

        audit = AuditCreate(
            audit_by=auditor.id,
            document_id=document_id
        )

        return self.create_audit_request(audit)

    def get_audit_status(self, document_id: int) -> ActionStatus:
        audit = AuditCRUD(self.db).get_audit_by_document_id(document_id)
        if not audit:
            raise AuditException.DocumentAuditNotFound({"document_id": document_id})

        return audit.status

    def get_all_audits_for_user_by_username(self, username: str) -> list[Type[AuditDB]]:
        user = UserCRUD(self.db).get_user(username)
        if not user:
            raise UserException.UserNotFound({"username": username})

        audits = AuditCRUD(self.db).get_audits_by_user(user.id)

        return audits

    def get_pending_audits_by_username(self, username: str) -> list[Type[AuditDB]]:
        user = UserCRUD(self.db).get_user(username)
        if not user:
            raise UserException.UserNotFound({"username": username})

        audits = AuditCRUD(self.db).get_audits_by_user_and_status(user.id, ActionStatus.PENDING)

        return audits

    def get_audited_documents_by_username(self, username: str) -> list[Type[AuditDB]]:
        user = UserCRUD(self.db).get_user(username)
        if not user:
            raise UserException.UserNotFound({"username": username})

        audits = AuditCRUD(self.db).get_audits_by_user_and_status(user.id, ActionStatus.DONE)

        return audits


class AuditCRUD(AppService):
    def create_audit(self, audit: AuditCreate) -> AuditDB:
        audit_db = self.db.query(AuditDB).filter(AuditDB.document_id == audit.document_id).first()
        if audit_db:
            raise AuditException.DocumentAuditAlreadyExists({"document_id": audit.document_id})

        auditdb = AuditDB(
            status=ActionStatus.PENDING,
            audited_by=audit.audit_by,
            document_id=audit.document_id,
            audited_at=None
        )

        self.db.add(auditdb)
        self.db.commit()
        self.db.refresh(auditdb)

        return auditdb

    def get_audit(self, audit_id: int) -> AuditDB | None:
        audit = self.db.query(AuditDB).filter(AuditDB.audit_id == audit_id).first()

        return audit

    def get_all_audits(self) -> list[Type[AuditDB]]:
        audits = self.db.query(AuditDB).all()

        return audits

    def get_audits_by_user(self, user_id: int) -> list[Type[AuditDB]]:
        audits = self.db.query(AuditDB).filter(AuditDB.audited_by == user_id).all()

        return audits

    def get_audits_by_status(self, status: ActionStatus) -> list[Type[AuditDB]]:
        audits = self.db.query(AuditDB).filter(AuditDB.status == status).all()

        return audits

    def get_audits_by_user_and_status(self, user_id: int, status: ActionStatus) -> list[Type[AuditDB]]:
        audits = self.db.query(AuditDB).filter(AuditDB.audited_by == user_id, AuditDB.status == status).all()

        return audits

    def get_audit_by_document_id(self, document_id: int) -> AuditDB | None:
        audit = self.db.query(AuditDB).filter(AuditDB.document_id == document_id).first()

        return audit

    def update_audit(self, audit: AuditDB) -> AuditDB:
        self.db.commit()
        self.db.refresh(audit)

        return audit

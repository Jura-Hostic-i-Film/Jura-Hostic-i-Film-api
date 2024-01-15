from app.schemas.signatures import SignatureCreate, Signature
from app.services.archives import ArchiveService
from app.services.documents import DocumentService
from app.services.main import AppService
from typing import Type
from app.models.signatures import SignatureDB
from app.services.users import UserService
from app.utils.enums import ActionStatus, DocumentStatusEnum, RolesEnum
from datetime import datetime
from app.schemas.signatures import Signature
import app.services.documents as documents

from app.utils.exceptions.signature_exceptions import SignatureException
from app.utils.exceptions.user_exceptions import UserException


class SignatureCRUD(AppService):
    def get_all_signatures(self) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).all()

    def get_signatures_by_status(self, status: ActionStatus) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).filter(status == SignatureDB.status).all()

    def get_signatures_by_user(self, user_id: int) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).filter(user_id == SignatureDB.sign_by).all()

    def get_signatures_by_user_and_status(self, user_id: int, status: ActionStatus) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).filter(user_id == SignatureDB.sign_by, status == SignatureDB.status).all()

    def create_signature(self, signature: SignatureCreate) -> SignatureDB:
        signature_db = self.db.query(SignatureDB).filter(SignatureDB.document_id == signature.document_id).first()
        if signature_db:
            raise SignatureException.DocumentSignatureAlreadyExists({"document_id": signature.document_id})

        signatureDB = SignatureDB(
            status=ActionStatus.PENDING,
            sign_by=signature.sign_by,
            document_id=signature.document_id,
            signed_at=None
        )

        self.db.add(signatureDB)
        self.db.commit()
        self.db.refresh(signatureDB)
        return signatureDB

    def get_signed_by_document_id(self, document_id: int) -> SignatureDB | None:
        return self.db.query(SignatureDB).filter(document_id == SignatureDB.document_id).first()

    def update_signature(self, signature: SignatureDB) -> Signature:
        self.db.commit()
        self.db.refresh(signature)
        return signature


class SignatureService(AppService):
    def get_all_signatures(self) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_all_signatures()

    def get_all_pending_signatures(self) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_status(ActionStatus.PENDING)

    def get_all_signed_documents(self) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_status(ActionStatus.DONE)

    def get_all_signatures_for_user_by_id(self, user_id: int) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_user(user_id)

    def get_all_signatures_for_user_by_username(self, username: str) -> list[Type[SignatureDB]]:
        user = UserService(self.db).get_user(username)

        if not user:
            raise UserException.UserNotFound({"username": username})

        user_id = user.id
        return SignatureCRUD(self.db).get_signatures_by_user(user_id)

    def get_pending_signatures_by_username(self, username: str) -> list[Type[SignatureDB]]:
        user = UserService(self.db).get_user(username)

        if not user:
            raise UserException.UserNotFound({"username": username})

        user_id = user.id
        return SignatureCRUD(self.db).get_signatures_by_user_and_status(user_id, ActionStatus.PENDING)

    def get_pending_signatures_by_id(self, user_id: int) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_user_and_status(user_id, ActionStatus.PENDING)

    def get_signed_documents_by_username(self, username: str) -> list[Type[SignatureDB]]:
        user = UserService(self.db).get_user(username)

        if not user:
            raise UserException.UserNotFound({"username": username})

        user_id = user.id
        return SignatureCRUD(self.db).get_signatures_by_user_and_status(user_id, ActionStatus.DONE)

    def get_signed_documents_by_id(self, user_id: int) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_user_and_status(user_id, ActionStatus.DONE)

    def get_signed_by_document_id(self, document_id: int) -> SignatureDB:
        signature = SignatureCRUD(self.db).get_signed_by_document_id(document_id)

        if not signature:
            raise SignatureException.DocumentSignatureNotFound({"document_id": document_id})

        return signature

    def get_signature_status(self, document_id: int) -> ActionStatus:
        signature = SignatureCRUD(self.db).get_signed_by_document_id(document_id)
        if not signature:
            raise SignatureException.DocumentSignatureNotFound({"document_id": document_id})
        return signature.status

    def sign_document(self, document_id: int, username: str) -> Signature:
        signature = SignatureCRUD(self.db).get_signed_by_document_id(document_id)
        document = DocumentService(self.db).get_document(document_id)
        user = UserService(self.db).get_user_by_id(signature.sign_by)

        if not user:
            raise UserException.UserNotFound({"user_id": signature.sign_by})

        if username != user.username:
            raise UserException.UserNotAuthorized({"username": username})

        if not signature:
            raise SignatureException.DocumentSignatureNotFound({"document_id": document_id})

        if signature.status == ActionStatus.DONE:
            raise SignatureException.DocumentAlreadySigned({"document_id": document_id})

        signature.status = ActionStatus.DONE
        signature.signed_at = datetime.now()

        SignatureCRUD(self.db).update_signature(signature)
        documents.DocumentService(self.db).update_document(document_id, DocumentStatusEnum.SIGNED)

        ArchiveService(self.db).create_archive_for_document(document_id, document.document_type)

        return signature

    def create_signature_request(self, signature: SignatureCreate) -> SignatureDB:
        user = UserService(self.db).get_user_by_id(signature.sign_by)

        if not user:
            raise UserException.UserNotFound({"user_id": signature.sign_by})

        roles = [RolesEnum(role.name) for role in user.roles]

        if (RolesEnum.ADMIN not in roles) and (RolesEnum.DIRECTOR not in roles):
            raise UserException.UserNotAuthorized({"user_id": signature.sign_by})

        return SignatureCRUD(self.db).create_signature(signature)

    def create_signature_for_document(self, document_id: int) -> SignatureDB:
        directors = UserService(self.db).get_users([RolesEnum.ADMIN])

        if not directors:
            raise UserException.NoUsersWithRole({"role": RolesEnum.DIRECTOR})

        signs_with_pending_signatures = []

        for director in directors:
            pending_signatures = self.get_pending_signatures_by_id(director.id)
            if pending_signatures:
                signs_with_pending_signatures.append((director, len(pending_signatures)))
            else:
                signs_with_pending_signatures.append((director, 0))

        director = min(signs_with_pending_signatures, key=lambda x: x[1])[0]

        signature = SignatureCreate(
            sign_by=director.id,
            document_id=document_id
        )

        return self.create_signature_request(signature)

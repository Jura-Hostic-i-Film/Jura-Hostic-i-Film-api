from app.schemas.signatures import SignatureCreate, Signature
from app.services.main import AppService
from typing import Type
from app.models.signatures import SignatureDB
from app.utils.enums import ActionStatus
from datetime import datetime
from pydantic import BaseModel
from app.schemas.signatures import Signature

from app.utils.exceptions.signature_exceptions import SignatureException


class SignatureCRUD(AppService):
    def get_all_signatures(self) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).all()

    def get_signatures_by_status(self, status: ActionStatus) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).filter(status == SignatureDB.status).all()

    def get_signatures_by_user(self, username: str) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).filter(username == SignatureDB.sign_by).all()

    def get_signatures_by_user_and_status(self, username: str, status: ActionStatus) -> list[Type[SignatureDB]]:
        return self.db.query(SignatureDB).filter(username == SignatureDB.sign_by, status == SignatureDB.status).all()

    def create_signature(self, signature: SignatureCreate) -> SignatureDB:
        signature_db = self.db.query(SignatureDB).filter(SignatureDB.document_id == signature.document_id).first()
        if signature_db:
            raise SignatureException.DocumentSignatureAlreadyExists({"document_id": signature.document_id})

        signatureDB = SignatureDB(
            status=ActionStatus.PENDING,
            sign_by=signature.sign_by,
            document_id=signature.document_id
        )

        self.db.add(signatureDB)
        self.db.commit()
        self.db.refresh(signatureDB)
        return signatureDB

    def get_signed_by_document_id(self, document_id: int) -> Type[SignatureDB]:
        return self.db.query(SignatureDB).filter(document_id == SignatureDB.document_id)

    def update_signature(self, signature: SignatureDB) -> Signature:
        self.db.commit()
        self.db.refresh(signature)
        return True


class SignatureService(AppService):
    def get_all_signatures(self) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_all_signatures()

    def get_all_pending_signatures(self) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_status(ActionStatus.PENDING)

    def get_all_signed_documents(self) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_status(ActionStatus.DONE)

    def get_all_signatures_for_user(self, username: str) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_user(username)

    def get_pending_signatures(self, username: str) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_user_and_status(username, ActionStatus.PENDING)

    def get_signed_documents(self, username: str) -> list[Type[SignatureDB]]:
        return SignatureCRUD(self.db).get_signatures_by_user_and_status(username, ActionStatus.DONE)

    def get_signature_status(self, document_id: int) -> ActionStatus:
        signature = SignatureCRUD(self.db).get_signed_by_document_id(document_id)
        if not signature:
            raise SignatureException.DocumentSignatureNotFound({"document_id": document_id})
        return signature.signature_status

    def sign_document(self, document_id: int) -> bool:
        signature = SignatureCRUD(self.db).get_signed_by_document_id(document_id)
        if not signature:
            raise SignatureException.DocumentSignatureNotFound({"document_id": document_id})

        signature.signature_status = ActionStatus.DONE
        signature.signed_at = datetime.now()
        return SignatureCRUD(self.db).update_signature(signature)

    def create_signature_request(self, signature_request: SignatureCreate) -> SignatureDB:
        return SignatureCRUD(self.db).create_signature(signature_request)

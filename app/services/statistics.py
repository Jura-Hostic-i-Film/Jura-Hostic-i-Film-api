from app.services.archives import ArchiveService
from app.services.audit import AuditService
from app.services.documents import DocumentService
from app.services.main import AppService
from app.services.signatures import SignatureService
from app.services.users import UserService
from app.utils.enums import RolesEnum, DocumentTypeEnum, ArchiveStatus


class StatisticsService(AppService):
    def get_user_statistics(self, username: str) -> dict:
        user = UserService(self.db).get_user(username)

        user_id = user.id

        statistics = dict()

        roles = [RolesEnum(role.name) for role in user.roles]

        scanned_documents = DocumentService(self.db).get_documents_by_user_id(user_id)
        statistics["scanned_documents"] = len(scanned_documents)

        if RolesEnum.AUDITOR in roles:
            audited_documents = AuditService(self.db).get_audited_documents(user_id)
            statistics["audited_documents"] = len(audited_documents)

        if RolesEnum.DIRECTOR in roles:
            signed_documents = SignatureService(self.db).get_signed_documents_by_id(user_id)
            statistics["signed_documents"] = len(signed_documents)

        if {RolesEnum.ACCOUNTANT_OFFER, RolesEnum.ACCOUNTANT_RECEIPT, RolesEnum.ACCOUNTANT_INTERNAL} & set(roles):
            archived_documents = ArchiveService(self.db).get_archives_by_user_and_status(user_id, ArchiveStatus.DONE)

            if RolesEnum.ACCOUNTANT_OFFER in roles:
                offers = [document for document in archived_documents if
                          document.document.document_type == DocumentTypeEnum.OFFER]
                statistics["archived_offers"] = len(offers)

            if RolesEnum.ACCOUNTANT_RECEIPT in roles:
                receipts = [document for document in archived_documents if
                            document.document.document_type == DocumentTypeEnum.RECEIPT]
                statistics["archived_receipts"] = len(receipts)

            if RolesEnum.ACCOUNTANT_INTERNAL in roles:
                internals = [document for document in archived_documents if
                             document.document.document_type == DocumentTypeEnum.INTERNAL]
                statistics["archived_internals"] = len(internals)

        return statistics

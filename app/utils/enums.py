from enum import Enum


class RolesEnum(str, Enum):
    ADMIN = 'admin'
    DIRECTOR = 'director'
    AUDITOR = 'auditor'
    ACCOUNTANT_RECEIPT = 'accountant_receipt'
    ACCOUNTANT_OFFER = 'accountant_offer'
    ACCOUNTANT_INTERNAL = 'accountant_internal'
    EMPLOYEE = 'employee'


class ActionStatus(str, Enum):
    PENDING = 'pending'
    DONE = 'done'


class ArchiveStatus(str, Enum):
    PENDING = 'pending'
    SIGNED_PENDING = 'signed_pending'
    DONE = 'done'
    AWAITING_SIGNATURE = 'awaiting_signature'


class DocumentTypeEnum(str, Enum):
    RECEIPT = 'receipt'
    OFFER = 'offer'
    INTERNAL = 'internal'


class DocumentStatusEnum(str, Enum):
    SCANNED = 'scanned'
    APPROVED = 'approved'
    REFUSED = 'refused'
    SIGNED = 'signed'
    AUDITED = 'audited'
    SIGNED_AND_ARCHIVED = 'signed_and_archived'
    ARCHIVED = 'archived'

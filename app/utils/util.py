from app.utils.enums import DocumentStatusEnum

COMPATIBLE_STATUSES = {
    DocumentStatusEnum.SCANNED: [DocumentStatusEnum.APPROVED, DocumentStatusEnum.REFUSED],
    DocumentStatusEnum.APPROVED: [DocumentStatusEnum.AUDITED],
    DocumentStatusEnum.REFUSED: [],
    DocumentStatusEnum.AUDITED: [DocumentStatusEnum.SIGNED, DocumentStatusEnum.ARCHIVED],
    DocumentStatusEnum.SIGNED: [DocumentStatusEnum.SIGNED_AND_ARCHIVED],
    DocumentStatusEnum.SIGNED_AND_ARCHIVED: [],
    DocumentStatusEnum.ARCHIVED: [],
}
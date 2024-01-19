from app.models.audit import AuditDB
from app.schemas.audit import Audit, AuditCreate
from app.utils.enums import ActionStatus
from tests.documents.util import document1, document2
from tests.users.util import director

audit1 = Audit(
    audit_id=1,
    audited_at=None,
    status=ActionStatus.PENDING,
    audited=director,
    document=document1,
)

audit2 = Audit(
    audit_id=2,
    audited_at="2021-01-01T00:00:00",
    status=ActionStatus.DONE,
    audited=director,
    document=document2,
)

audit_create = AuditCreate(
    audit_by=director.id,
    document_id=2,
)

audits = [audit1, audit2]

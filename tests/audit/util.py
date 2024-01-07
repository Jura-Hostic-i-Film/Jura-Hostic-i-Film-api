
from app.schemas.audit import Audit
from app.utils.enums import ActionStatus
from tests.users.util import user, director
from tests.documents.util import document1, document2

audit1 = Audit(
    audit_id=1,
    audited_at=None,
    audit_status=ActionStatus.PENDING,
    audited_by=user,
    document_id=1,
    document=document1
)

audit2 = Audit(
    audit_id=2,
    audited_at="2021-01-01T00:00:00",
    audit_status=ActionStatus.DONE,
    audited_by=director,
    document_id=2,
    document=document2
)

audits = [audit1, audit2]


from app.schemas.audit import Audit
from app.utils.enums import ActionStatus

audit1 = Audit(
    id=1,
    audited_at="2021-01-01T00:00:00",
    status=ActionStatus.PENDING,
    audited_by="test",
    document_id=1,
)

audit2 = Audit(
    id=2,
    audited_at="2021-01-01T00:00:00",
    status=ActionStatus.DONE,
    audited_by="test",
    document_id=1,
)

audits = [audit1, audit2]

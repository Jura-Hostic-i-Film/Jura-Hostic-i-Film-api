from datetime import datetime
from app.models.signatures import SignatureDB
from app.schemas.signatures import SignatureCreate
from app.utils.enums import ActionStatus
from tests.users.util import admin, director

signature1 = SignatureDB(
    signature_id=1,
    status=ActionStatus.PENDING,
    signed_at=datetime.now(),
    document_id=1,
    sign_by=admin.id,
)

signature2 = SignatureDB(
    signature_id=2,
    status=ActionStatus.DONE,
    signed_at=datetime.now(),
    document_id=2,
    sign_by=director.id,
)

signatures = [signature1, signature2]

signature_create = SignatureCreate(
    document_id=1,
    sign_by=director.id,
)

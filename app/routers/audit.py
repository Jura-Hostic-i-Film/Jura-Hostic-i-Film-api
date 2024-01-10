from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.schemas.audit import Audit, AuditCreate
from app.services.audit import AuditService
from app.utils.enums import ActionStatus, RolesEnum

router = APIRouter(
    prefix="/audits",
    tags=["audits"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_audits(usr: str | None = None, status: ActionStatus | None = None, db: get_db = Depends(),
                     credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Audit]:
    if usr is None and status is None:
        result = AuditService(db).get_all_audits()

    if usr is None and status is not None:
        if status == ActionStatus.PENDING:
            result = AuditService(db).get_all_pending_audits()
        else:
            result = AuditService(db).get_all_audited_documents()

    if usr is not None and status is None:
        result = AuditService(db).get_all_audits_for_user(usr)

    if usr is not None and status is not None:
        if status == ActionStatus.PENDING:
            result = AuditService(db).get_pending_audits(usr)
        else:
            result = AuditService(db).get_audited_documents(usr)

    return result


@router.get("/me")
@authenticate()
async def me(status: ActionStatus | None = None, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Audit]:
    username = credentials["username"]
    if status is None:
        result = AuditService(db).get_all_audits_for_user(username)
    elif status == ActionStatus.PENDING:
        result = AuditService(db).get_pending_audits(username)
    else:
        result = AuditService(db).get_audited_documents(username)

    return result


@router.post("/create")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def create_audit_request(audit: AuditCreate, db: get_db = Depends(),
                               credentials: JwtAuthorizationCredentials = Security(access_security)) -> Audit:
    result = AuditService(db).create_audit_request(audit)
    return result


@router.post("/{document_id}")
@authenticate([RolesEnum.ADMIN, RolesEnum.AUDITOR])
async def audit_document(document_id: int, db: get_db = Depends(),
                         credentials: JwtAuthorizationCredentials = Security(access_security)) -> bool:
    result = AuditService(db).audit_document(document_id)
    return result

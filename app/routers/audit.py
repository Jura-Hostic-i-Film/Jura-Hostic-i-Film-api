from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.schemas.audit import Audit, AuditCreate, DocumentSummary
from app.services.audit import AuditService
from app.utils.enums import ActionStatus, RolesEnum

router = APIRouter(
    prefix="/audits",
    tags=["audits"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_audits(user_id: int | None = None, status: ActionStatus | None = None, db: get_db = Depends(),
                     credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Audit]:
    if user_id is None and status is None:
        result = AuditService(db).get_all_audits()

    if user_id is None and status is not None:
        if status == ActionStatus.PENDING:
            result = AuditService(db).get_all_pending_audits()
        else:
            result = AuditService(db).get_all_audited_documents()

    if user_id is not None and status is None:
        result = AuditService(db).get_all_audits_for_user(user_id)

    if user_id is not None and status is not None:
        if status == ActionStatus.PENDING:
            result = AuditService(db).get_pending_audits(user_id)
        else:
            result = AuditService(db).get_audited_documents(user_id)

    return result


@router.get("/me")
@authenticate()
async def me(status: ActionStatus | None = None, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Audit]:
    username = credentials["username"]
    if status is None:
        result = AuditService(db).get_all_audits_for_user_by_username(username)
    elif status == ActionStatus.PENDING:
        result = AuditService(db).get_pending_audits_by_username(username)
    else:
        result = AuditService(db).get_audited_documents_by_username(username)

    return result


@router.get("/me/pending")
@authenticate()
async def me_pending_count(db: get_db = Depends(),
                           credentials: JwtAuthorizationCredentials = Security(access_security)) -> int:
    username = credentials["username"]
    result = AuditService(db).get_pending_audits_by_username(username)

    return len(result)


@router.post("/create")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def create_audit_request(audit: AuditCreate, db: get_db = Depends(),
                               credentials: JwtAuthorizationCredentials = Security(access_security)) -> Audit:
    result = AuditService(db).create_audit_request(audit)
    return result


@router.post("/{document_id}")
@authenticate([RolesEnum.ADMIN, RolesEnum.AUDITOR])
async def audit_document(document_id: int, document_summary: DocumentSummary | None = None,
                         db: get_db = Depends(),
                         credentials: JwtAuthorizationCredentials = Security(access_security)) -> Audit:
    result = AuditService(db).audit_document(document_id, credentials["username"], document_summary)
    return result


@router.get("/{document_id}")
@authenticate()
async def get_audit(document_id: int, db: get_db = Depends(),
                    credentials: JwtAuthorizationCredentials = Security(access_security)) -> Audit:
    result = AuditService(db).get_audit_by_document_id(document_id)
    return result

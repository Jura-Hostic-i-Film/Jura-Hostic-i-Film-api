from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.schemas.signatures import SignatureCreate, Signature
from app.services.signatures import SignatureService
from app.utils.enums import RolesEnum, ActionStatus
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

router = APIRouter(
    prefix="/signatures",
    tags=["signatures"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_signatures(user_id: int | None = None,
                         status: ActionStatus | None = None,
                         db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Signature]:
    if user_id is None and status is None:
        result = SignatureService(db).get_all_signatures()

    elif user_id is None and status is not None:
        if status == ActionStatus.PENDING:
            result = SignatureService(db).get_all_pending_signatures()
        elif status == ActionStatus.DONE:
            result = SignatureService(db).get_all_signed_documents()

    elif user_id is not None and status is None:
        result = SignatureService(db).get_all_signatures_for_user_by_id(user_id)

    elif user_id is not None and status is not None:
        if status == ActionStatus.PENDING:
            result = SignatureService(db).get_pending_signatures_by_id(user_id)
        elif status == ActionStatus.DONE:
            result = SignatureService(db).get_signed_documents_by_id(user_id)

    return result


@router.post("/create")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def create_signature(signature: SignatureCreate, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> Signature:
    return SignatureService(db).create_signature_request(signature)


@router.get("/me")
@authenticate()
async def me(status: ActionStatus | None = None, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Signature]:
    username = credentials["username"]
    if status is None:
        result = SignatureService(db).get_all_signatures_for_user_by_username(username)
    elif status == ActionStatus.PENDING:
        result = SignatureService(db).get_pending_signatures_by_username(username)
    elif status == ActionStatus.DONE:
        result = SignatureService(db).get_signed_documents_by_username(username)
    return result


@router.get("/me/pending")
@authenticate()
async def me_pending_count(db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> int:
    username = credentials["username"]
    result = SignatureService(db).get_pending_signatures_by_username(username)

    return len(result)


@router.post("/{document_id}")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def sign_document(document_id: int, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> Signature:
    username = credentials["username"]
    return SignatureService(db).sign_document(document_id, username)

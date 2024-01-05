from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.schemas.signatures import SignatureCreate, Signature
from app.services.signatures import SignatureService
from app.utils.enums import RolesEnum, ActionStatus
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter(
    prefix="/signatures",
    tags=["signatures"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_signatures(user: str | None = None,
                         status: ActionStatus | None = None,
                         db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Signature]:
    if user is None and status is None:
        result = SignatureService(db).get_all_signatures()

    elif user is None and status is not None:
        if status == ActionStatus.PENDING:
            result = SignatureService(db).get_all_pending_signatures()
        elif status == ActionStatus.DONE:
            result = SignatureService(db).get_all_signed_documents()

    elif user is not None and status is None:
        result = SignatureService(db).get_all_signatures_for_user(user)

    elif user is not None and status is not None:
        if status == ActionStatus.PENDING:
            result = SignatureService(db).get_pending_signatures(user)
        elif status == ActionStatus.DONE:
            result = SignatureService(db).get_signed_documents(user)

    return result


@router.post("/create")
@authenticate()
async def create_signature(signature: SignatureCreate, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> Signature:
    return SignatureService(db).create_signature_request(signature)


@router.get("/me")
@authenticate()
async def me(status: ActionStatus | None = None, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Signature]:
    username = credentials["username"]
    if status is None:
        result = SignatureService(db).get_all_signatures_for_user(username)
    elif status == ActionStatus.PENDING:
        result = SignatureService(db).get_pending_signatures(username)
    elif status == ActionStatus.DONE:
        result = SignatureService(db).get_signed_documents(username)
    return result


@router.post("/signature/{document_id}")
@authenticate()
async def sign_document(document_id: int, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> bool:
    return SignatureService(db).sign_document(document_id)

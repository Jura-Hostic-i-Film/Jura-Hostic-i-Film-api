from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.services.archives import ArchiveService
from app.utils.enums import RolesEnum, ArchiveStatus
from app.schemas.archives import ArchiveCreate, Archive

router = APIRouter(
    prefix="/archives",
    tags=["archives"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_archives(user_id: int | None = None,
                       status: ArchiveStatus | None = None,
                       db: get_db = Depends(),
                       credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Archive]:
    if user_id is None and status is None:
        result = ArchiveService(db).get_all_archives()

    elif user_id is None and status is not None:
        result = ArchiveService(db).get_archives_by_status(status)

    elif user_id is not None and status is None:
        result = ArchiveService(db).get_all_archives_for_user_by_id(user_id)

    elif user_id is not None and status is not None:
        result = ArchiveService(db).get_archives_by_user_and_status(user_id, status)

    return result


@router.post("/create")
@authenticate()
async def create_archive(archive: ArchiveCreate, db: get_db = Depends(),
                         credentials: JwtAuthorizationCredentials = Security(access_security)) -> Archive:
    return ArchiveService(db).create_archive_request(archive)


@router.get("/me")
@authenticate()
async def me(status: ArchiveStatus | None = None, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Archive]:
    username = credentials["username"]
    if status is None:
        result = ArchiveService(db).get_all_archives_for_user_by_username(username)
    elif status == ArchiveStatus.PENDING or status == ArchiveStatus.SIGNED_PENDING:
        result = ArchiveService(db).get_pending_archives_by_username(username)
    elif status == ArchiveStatus.DONE:
        result = ArchiveService(db).get_archived_documents_by_username(username)
    elif status == ArchiveStatus.AWAITING_SIGNATURE:
        result = ArchiveService(db).get_archives_awaiting_signature_by_username(username)
    return result


@router.get("/me/pending")
async def me_pending_count(db: get_db = Depends(),
                           credentials: JwtAuthorizationCredentials = Security(access_security)) -> int:
    username = credentials["username"]
    result = ArchiveService(db).get_pending_archives_by_username(username)
    return len(result)


@router.get("/{document_id}")
@authenticate()
async def get_archive(document_id: int, db: get_db = Depends(),
                      credentials: JwtAuthorizationCredentials = Security(access_security)) -> Archive:
    return ArchiveService(db).get_archive_by_document_id(document_id)


@router.post("/archive/{document_id}/{status}")
@authenticate()
async def archive_document(document_id: int, status: ArchiveStatus, db: get_db = Depends(),
                           credentials: JwtAuthorizationCredentials = Security(access_security)) -> Archive:
    return ArchiveService(db).archive_document(document_id, status, credentials["username"])

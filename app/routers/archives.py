from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.services.archives import ArchiveService
from app.utils.enums import RolesEnum, ActionStatus
from app.schemas.archives import ArchiveCreate, Archive

router = APIRouter(
    prefix="/archives",
    tags=["archives"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_archives(user_id: int | None = None,
                       status: ActionStatus | None = None,
                       db: get_db = Depends(),
                       credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Archive]:
    if user_id is None and status is None:
        result = ArchiveService(db).get_all_archives()

    elif user_id is None and status is not None:
        if status == ActionStatus.PENDING:
            result = ArchiveService(db).get_all_pending_archives()
        elif status == ActionStatus.DONE:
            result = ArchiveService(db).get_all_archived_documents()

    elif user_id is not None and status is None:
        result = ArchiveService(db).get_all_archives_for_user_by_id(user_id)

    elif user_id is not None and status is not None:
        if status == ActionStatus.PENDING:
            result = ArchiveService(db).get_pending_archives_by_id(user_id)
        elif status == ActionStatus.DONE:
            result = ArchiveService(db).get_archived_documents_by_id(user_id)

    return result


@router.post("/create")
@authenticate()
async def create_archive(archive: ArchiveCreate, db: get_db = Depends(),
                         credentials: JwtAuthorizationCredentials = Security(access_security)) -> Archive:
    return ArchiveService(db).create_archive_request(archive)


@router.get("/me")
@authenticate()
async def me(status: ActionStatus | None = None, db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Archive]:
    username = credentials["username"]
    if status is None:
        result = ArchiveService(db).get_all_archives_for_user_by_username(username)
    elif status == ActionStatus.PENDING:
        result = ArchiveService(db).get_pending_archives_by_username(username)
    elif status == ActionStatus.DONE:
        result = ArchiveService(db).get_archived_documents_by_username(username)
    return result


@router.get("/me/pending")
@authenticate()
async def me_pending(db: get_db = Depends(),
                     credentials: JwtAuthorizationCredentials = Security(access_security)) -> int:
    username = credentials["username"]
    result = ArchiveService(db).get_pending_archives_by_username(username)
    return len(result)


@router.post("/archive/{document_id}")
@authenticate()
async def archive_document(document_id: int, db: get_db = Depends(),
                           credentials: JwtAuthorizationCredentials = Security(access_security)) -> Archive:
    return ArchiveService(db).archive_document(document_id)

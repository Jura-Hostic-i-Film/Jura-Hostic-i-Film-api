from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.config.database import get_db
from app.config.jwt import access_security
from app.decorators.authenticate import authenticate
from app.schemas.documents import Document, DocumentCreate
from app.services.documents import DocumentService
from app.utils.enums import RolesEnum, DocumentTypeEnum, DocumentStatusEnum

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
@authenticate([RolesEnum.ADMIN, RolesEnum.DIRECTOR])
async def get_all_documents(document_type: DocumentTypeEnum | None = None,
                            document_status: DocumentStatusEnum | None = None,
                            db: get_db = Depends(),
                            credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Document]:
    result = DocumentService(db).get_all_documents(document_type, document_status)
    return result


@router.get("/me")
@authenticate()
async def me(db: get_db = Depends(),
             credentials: JwtAuthorizationCredentials = Security(access_security)) -> list[Document]:
    username = credentials["username"]
    result = DocumentService(db).get_documents(username)
    return result


@router.post("/create")
@authenticate()
async def create_document(document: DocumentCreate, db: get_db = Depends(),
                          credentials: JwtAuthorizationCredentials = Security(access_security)) -> Document:
    username = credentials["username"]
    result = DocumentService(db).create_document(document, username)
    return result
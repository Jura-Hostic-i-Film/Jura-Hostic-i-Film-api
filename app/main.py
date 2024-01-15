from fastapi import FastAPI
from app.utils.exceptions.app_exceptions import AppExceptionCase, app_exception_handler
from app.utils.startup import create_tables, add_roles

import app.routers.users as users
import app.routers.documents as documents
import app.routers.signatures as signatures
import app.routers.audit as audit
import app.routers.archives as archives

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    create_tables()
    add_roles()


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)

app.include_router(users.router)
app.include_router(documents.router)
app.include_router(audit.router)
app.include_router(signatures.router)
app.include_router(archives.router)

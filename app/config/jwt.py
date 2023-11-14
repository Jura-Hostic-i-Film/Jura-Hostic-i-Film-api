from datetime import timedelta

from fastapi_jwt import JwtAccessBearerCookie

from app.config.base import settings

access_security = JwtAccessBearerCookie(
    secret_key=settings.secret_key,
    auto_error=False,
    access_expires_delta=timedelta(hours=settings.access_token_expire_hours)  # change access token validation timedelta
)
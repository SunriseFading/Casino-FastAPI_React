from datetime import datetime, timedelta

from jose import jwt
from datetime import timezone
from src.settings import jwt_settings
from fastapi_jwt import (
    JwtAccessBearer,
    JwtRefreshCookie,
)


access_security = JwtAccessBearer(
    secret_key=jwt_settings.secret_key,
    auto_error=True,
    access_expires_delta=timedelta(minutes=jwt_settings.access_token_expires)
)

refresh_security = JwtRefreshCookie(
    secret_key=jwt_settings.secret_key,
    auto_error=True,
    refresh_expires_delta=timedelta(days=jwt_settings.refresh_token_expires),
)




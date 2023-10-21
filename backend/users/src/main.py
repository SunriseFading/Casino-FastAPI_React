from typing import Any

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import create_postgres_session
from src.routers import users
from src.settings import app_settings


def create_app() -> FastAPI:
    app_configuration: dict[str, Any] = {
        "title": app_settings.title,
        "root_path": app_settings.root_path,
    }
    if not app_settings.debug:
        app_configuration.update({"docs_url": None, "redoc_url": None})

    app = FastAPI(**app_configuration)

    app.include_router(users.router)

    @app.get("/healthcheck")
    async def healthcheck(
        session: AsyncSession = Depends(create_postgres_session),  # noqa: B008
    ) -> JSONResponse:
        return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)

    return app

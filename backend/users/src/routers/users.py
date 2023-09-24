from fastapi import APIRouter, Depends, Response, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.auth import access_security, refresh_security
from src.database.session import create_postgres_session
from src.schemas.users import UserLoginSchema, UserRegisterSchema, UserResponseSchema
from src.services.users import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    path="/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Register",
)
async def register(
    response: Response,
    schema: UserRegisterSchema,
    postgres_session: AsyncSession = Depends(create_postgres_session),
):
    return await user_service.register(
        response=response,
        schema=schema,
        session=postgres_session,
    )


@router.post(
    path="/login",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Login",
)
async def login(
    response: Response,
    schema: UserLoginSchema,
    postgres_session: AsyncSession = Depends(create_postgres_session),
):
    return await user_service.login(
        response=response,
        schema=schema,
        session=postgres_session,
    )


@router.get(
    path="/refresh",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Refresh token",
)
async def refresh(
    response: Response,
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
    postgres_session: AsyncSession = Depends(create_postgres_session),
):
    return await user_service.refresh(
        response=response,
        credentials=credentials,
        session=postgres_session,
    )


@router.get(
    path="/current",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user from access token",
)
async def current(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    postgres_session: AsyncSession = Depends(create_postgres_session),
):
    return await user_service.current(credentials=credentials, session=postgres_session)

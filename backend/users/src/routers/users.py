from fastapi import APIRouter, Depends, status, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import create_postgres_session
from src.schemas.users import UserLoginSchema, UserRegisterSchema, UserResponseSchema
from src.services.users import user_service
from src.core.auth import access_security, refresh_security
from fastapi_jwt import JwtAuthorizationCredentials


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
    schema: UserRegisterSchema,
    postgres_session: AsyncSession = Depends(create_postgres_session),
):
    return await user_service.register(
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
    schema: UserLoginSchema,
    postgres_session: AsyncSession = Depends(create_postgres_session),
):
    return await user_service.login(
        schema=schema,
        session=postgres_session,
    )


# @router.post(
#     path="/refresh",
#     response_model=UserResponseSchema,
#     status_code=status.HTTP_200_OK,
#     summary="Refresh token",
# )
# async def refresh(
#     credentials: JwtAuthorizationCredentials = Security(refresh_security),
#     postgres_session: AsyncSession = Depends(create_postgres_session),
# ):
#     return await user_service.refresh(
#         schema=credentials,
#         session=postgres_session,
#     )


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
    return await user_service.get(username=credentials["username"], session=postgres_session)

from fastapi import Response
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers.users import UserController, user_controller
from src.core.auth import access_security, refresh_security
from src.core.errors import UsernameAlreadyExists, UsernameNotExist, WrongPassword
from src.core.password import hash_password, verify_password
from src.database.models.users import User as UserModel
from src.schemas.users import UserLoginSchema, UserRegisterSchema, UserResponseSchema


class UserService:
    def __init__(self, controller: UserController) -> None:
        self.controller = controller

    async def create(
        self, schema: UserRegisterSchema, session: AsyncSession, raw: bool = False
    ) -> UserResponseSchema | UserModel:
        return await self.controller.create(schema=schema, session=session, raw=raw)

    async def get(self, session: AsyncSession, raw: bool = False, **kwargs) -> UserResponseSchema | UserModel | None:
        if user := await self.controller.get(**kwargs, session=session, raw=raw):
            return user
        return None

    async def register(
        self, response: Response, schema: UserRegisterSchema, session: AsyncSession
    ) -> UserResponseSchema:
        if await self.controller.get(username=schema.username, session=session, raw=False):
            raise UsernameAlreadyExists

        schema.password = hash_password(password=schema.password)
        user = await self.controller.create(schema=schema, session=session, raw=False)

        user.access_token = access_security.create_access_token(subject={"username": user.username})
        refresh_token = refresh_security.create_refresh_token(subject={"username": user.username})
        refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)

        return user

    async def login(self, response: Response, schema: UserLoginSchema, session: AsyncSession) -> UserResponseSchema:
        if user := await self.controller.get(username=schema.username, session=session, raw=True):
            if verify_password(plain_password=schema.password, hashed_password=user.password):
                response_schema = self.controller.to_schema(**user.__dict__)

                response_schema.access_token = access_security.create_access_token(
                    subject={"username": response_schema.username}
                )
                refresh_token = refresh_security.create_refresh_token(subject={"username": response_schema.username})
                refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)

                return response_schema

            raise WrongPassword

        raise UsernameNotExist

    async def refresh(
        self,
        response: Response,
        credentials: JwtAuthorizationCredentials,
        session: AsyncSession,
    ) -> UserResponseSchema | None:
        if response_schema := await self.controller.get(username=credentials["username"], session=session, raw=False):
            response_schema.access_token = access_security.create_access_token(subject=credentials.subject)
            refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)
            refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)
            return response_schema
        return None

    async def current(
        self, credentials: JwtAuthorizationCredentials, session: AsyncSession
    ) -> UserResponseSchema | None:
        if response := await self.controller.get(username=credentials["username"], session=session, raw=False):
            return response
        return None


user_service = UserService(controller=user_controller)

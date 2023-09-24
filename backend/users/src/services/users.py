from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users import UserLoginSchema, UserRegisterSchema
from src.controllers.users import user_controller
from src.core.password import hash_password, verify_password
from src.core.auth import access_security, refresh_security
from fastapi_jwt import JwtAuthorizationCredentials


class UserService:
    def __init__(self, controller):
        self.controller = controller

    async def create(self, schema: UserRegisterSchema, session: AsyncSession, raw: bool = False):
        return await self.controller.create(schema=schema, session=session, raw=raw)

    async def get(self, session: AsyncSession, raw: bool = False, **kwargs):
        if response := await self.controller.get(**kwargs, session=session, raw=raw):
            return response
        return None

    async def register(self, response: Response, schema: UserRegisterSchema, session: AsyncSession):
        schema.password = hash_password(password=schema.password)
        response_schema = await self.create(schema=schema, session=session, raw=False)
        response_schema.access_token = access_security.create_access_token(subject={"username": response_schema.username})
        refresh_token = refresh_security.create_refresh_token(subject={"username": response_schema.username})
        refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)
        return response_schema

    async def login(self, response: Response, schema: UserLoginSchema, session: AsyncSession):
        username = schema.username
        if model := await self.get(username=username, session=session, raw=True):
            if verify_password(plain_password=schema.password, hashed_password=model.password):
                response_schema = self.controller.to_schema(**model.__dict__)
                response_schema.access_token = access_security.create_access_token(subject={"username": response_schema.username})
                refresh_token = refresh_security.create_refresh_token(subject={"username": response_schema.username})
                refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)
                return response_schema

    async def refresh(self, response: Response, credentials: JwtAuthorizationCredentials, session: AsyncSession):
        username = credentials["username"]
        if response_schema := await self.get(username=username, session=session, raw=False):
            response_schema.access_token = access_security.create_access_token(subject=credentials.subject)
            refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)
            refresh_security.set_refresh_cookie(response=response, refresh_token=refresh_token)
            return response_schema

    async def current(self, credentials: JwtAuthorizationCredentials, session: AsyncSession):
        username = credentials["username"]
        if response := await self.get(username=username, session=session, raw=False):
            return response


user_service = UserService(controller=user_controller)

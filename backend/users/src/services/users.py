from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.users import UserLoginSchema, UserRegisterSchema
from src.controllers.users import user_controller
from src.core.password import hash_password, verify_password
from src.core.auth import access_security, refresh_security


class UserService:
    def __init__(self, controller):
        self.controller = controller

    async def create(self, schema: UserRegisterSchema, session: AsyncSession, raw: bool = False):
        return await self.controller.create(schema=schema, session=session, raw=raw)

    async def get(self, session: AsyncSession, raw: bool = False, **kwargs):
        if response := await self.controller.get(**kwargs, session=session, raw=raw):
            return response
        return None

    async def register(self, schema: UserRegisterSchema, session: AsyncSession):
        schema.password = hash_password(password=schema.password)
        response = await self.create(schema=schema, session=session, raw=False)
        response.access_token = access_security.create_access_token(subject={"username": response.username})
        response.refresh_token = refresh_security.create_refresh_token(subject={"username": response.username})
        return response

    async def login(self, schema: UserLoginSchema, session: AsyncSession):
        username = schema.username
        if model := await self.get(username=username, session=session, raw=True):
            if verify_password(plain_password=schema.password, hashed_password=model.password):
                response = self.controller.to_schema(**model.__dict__)
                response.access_token = access_security.create_access_token(subject={"username": response.username})
                response.refresh_token = refresh_security.create_refresh_token(subject={"username": response.username})
                return response


user_service = UserService(controller=user_controller)

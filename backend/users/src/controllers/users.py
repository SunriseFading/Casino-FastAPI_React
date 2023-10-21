from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.users import User as UserModel
from src.repositories.users import UserRepository, user_repository
from src.schemas.users import UserRegisterSchema, UserResponseSchema


class UserController:
    def __init__(self, schema: UserResponseSchema, model: UserModel, repository: UserRepository) -> None:
        self.schema = schema
        self.model = model
        self.repository = repository

    def to_schema(self, **kwargs: dict) -> UserResponseSchema:
        return self.schema(
            id=kwargs["id"],
            username=kwargs["username"],
        )

    def to_model(self, **kwargs: dict) -> UserModel:
        return self.model(
            username=kwargs["username"],
            password=kwargs["password"],
        )

    async def create(
        self, schema: UserRegisterSchema, session: AsyncSession, raw: bool = False
    ) -> UserResponseSchema | UserModel:
        model = self.to_model(**schema.model_dump())
        model = await self.repository.create(instance=model, session=session)
        return model if raw else self.to_schema(**model.__dict__)

    async def get(
        self, session: AsyncSession, raw: bool = False, **kwargs: dict[str, Any]
    ) -> UserResponseSchema | UserModel | None:
        if model := await self.repository.get(**kwargs, session=session):
            return model if raw else self.to_schema(**model.__dict__)
        return None


user_controller = UserController(schema=UserResponseSchema, model=UserModel, repository=user_repository)

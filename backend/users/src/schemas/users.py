from src.schemas.base import BaseSchema


class UserRegisterSchema(BaseSchema):
    username: str
    password: str


class UserLoginSchema(BaseSchema):
    username: str
    password: str


class UserResponseSchema(BaseSchema):
    id: int
    username: str
    access_token: str | None = None

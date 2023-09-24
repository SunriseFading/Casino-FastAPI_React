from src.database.models.users import User as UserModel
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    pass


user_repository = UserRepository(model=UserModel)

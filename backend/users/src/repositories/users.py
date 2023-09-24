from src.repositories.base import BaseRepository
from src.database.models.users import User as UserModel


class UserRepository(BaseRepository):
    pass


user_repository = UserRepository(model=UserModel)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(length=64), unique=True)
    password: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}"

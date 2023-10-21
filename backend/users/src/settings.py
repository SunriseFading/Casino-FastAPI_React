from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"


class AppSettings(Settings):
    title: str
    root_path: str
    debug: bool = True

    class Config:
        env_prefix = "app_"


class JWTSettings(Settings):
    secret_key: str
    header_type: str
    header_name: str
    algorithm: str
    access_token_expires: int
    refresh_token_expires: int | None = None

    class Config:
        env_prefix = "jwt_"


class PostgresSettings(Settings):
    user: str
    password: str
    host: str
    port: int
    db: str

    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    class Config:
        env_prefix = "postgres_"


app_settings = AppSettings()
jwt_settings = JWTSettings()
postgres_settings = PostgresSettings()

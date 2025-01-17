from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./tasks.db"

    class Config:
        env_file = ".env"

db = Settings()


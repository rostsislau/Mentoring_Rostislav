from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    db_url: str = "postgresql+asyncpg://tasks_user:mypass123@db/tasks"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./tasks.db"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()


    class Config:
        env_file = ".env"
        model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()



#**************************************************************************************************

# from pydantic_settings import BaseSettings
#
# class Settings(BaseSettings):
#     db_url: str = "sqlite+aiosqlite:///./tasks.db"
#     class Config:
#         env_file = ".env"
#
#
# config = Settings()

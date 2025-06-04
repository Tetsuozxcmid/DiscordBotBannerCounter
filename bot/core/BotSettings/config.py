from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str
    server_id: int
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

settings = Settings()
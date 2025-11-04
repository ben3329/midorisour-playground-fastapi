from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_nested_delimiter="__", env_file=".env"
    )


settings = Settings()

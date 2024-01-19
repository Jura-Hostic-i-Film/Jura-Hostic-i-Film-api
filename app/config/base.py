from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./sql_app.db"
    secret_key: str = "secret_key"
    access_token_expire_hours: int = 0
    DefaultEndpointsProtocol: str | None = None
    AccountName: str | None = None
    AccountKey: str | None = None
    EndpointSuffix: str | None = None
    image_path: str = "images"
    vision_key: str | None = None
    vision_endpoint: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

print(settings.database_url)
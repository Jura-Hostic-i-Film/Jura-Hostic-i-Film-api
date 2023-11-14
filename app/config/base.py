from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./sql_app.db"
    secret_key: str = "secret_key"
    access_token_expire_hours: int = 1


settings = Settings()

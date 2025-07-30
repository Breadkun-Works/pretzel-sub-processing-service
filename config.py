from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    APP_RELOAD: bool = False
    APP_TIMEOUT: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

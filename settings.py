# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ORS_API_KEY: str
    TOMORROW_API_KEY: str
    class Config:
        env_file = ".env"

settings = Settings()

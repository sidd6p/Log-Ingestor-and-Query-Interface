# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = r"sqlite:///./test.db"
    RABBITMQ_URL: str = r"amqp://guest:guest@http://localhost:15672/"

settings = Settings()

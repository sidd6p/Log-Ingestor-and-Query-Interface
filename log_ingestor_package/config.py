# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = r"sqlite:///./test.db"
    RABBITMQ_URL: str = r"amqp://guest:guest@localhost:5672"

settings = Settings()

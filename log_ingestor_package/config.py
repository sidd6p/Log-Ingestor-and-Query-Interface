# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DATABASE_URL: str = r"sqlite:///./test.db"
    DATABASE_URL: str = r"postgresql://postgres:sidd@localhost:5432/log_ingestor_package_db"
    RABBITMQ_URL: str = r"amqp://guest:guest@localhost:5672"

settings = Settings()

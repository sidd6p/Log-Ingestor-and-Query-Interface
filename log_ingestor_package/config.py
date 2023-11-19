from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "default_postgres_url")
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "default_elasticsearch_url")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:15672")


settings = Settings()

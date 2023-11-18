# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch
from log_ingestor_package import config

# SQLAlchemy Database Engine for PostgreSQL
engine = create_engine(
    config.settings.DATABASE_URL,  
    pool_size=20,  # Increase pool size
    max_overflow=40  # Increase max overflow
)

# SQLAlchemy Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy Base
Base = declarative_base()

# Elasticsearch Client
es_client = Elasticsearch(config.settings.ELASTICSEARCH_URL)

# models.py
from sqlalchemy import Column, Integer, String, JSON
from log_ingestor_package.database import Base, es_client


class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(String)
    resourceId = Column(String)
    timestamp = Column(String)
    traceId = Column(String)
    spanId = Column(String)
    commit = Column(String)
    # log_metadata = Column(JSON)  # Renamed from 'metadata' to 'log_metadata'


def create_elasticsearch_index():
    # Define the Elasticsearch index mapping
    mapping = {
        "mappings": {
            "properties": {
                "level": {"type": "keyword"},
                "message": {"type": "text"},
                "resourceId": {"type": "keyword"},
                # ... other fields ...
            }
        }
    }
    es_client.indices.create(index="log_entries", body=mapping, ignore=400)


def index_log_entry(log_entry):
    # Index a log entry in Elasticsearch
    doc = {
        "level": log_entry.level,
        "message": log_entry.message,
        "resourceId": log_entry.resourceId,
        # ... other fields ...
    }
    es_client.index(index="log_entries", document=doc)

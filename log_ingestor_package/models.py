# models.py
from sqlalchemy import Column, Integer, String, JSON
from log_ingestor_package.database import Base, es_client

class LogEntry(Base):
    __tablename__ = "logs_tb"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(String)
    resourceId = Column(String)
    timestamp = Column(String)
    traceId = Column(String)
    spanId = Column(String)
    commit = Column(String)
    meta_data = Column(JSON)  # Renamed from 'metadata'

def create_elasticsearch_index():
    mapping = {
        "mappings": {
            "properties": {
                "meta_data": {  # Add mapping for meta_data
                    "type": "nested",
                    "properties": {
                        "parentResourceId": {"type": "keyword"}
                    }
                }
                # ... other fields ...
            }
        }
    }
    es_client.indices.create(index="log_entries", body=mapping, ignore=400)

def index_log_entry(log_entry):
    doc = {
        "meta_data": log_entry.meta_data,  # Ensure meta_data is included
        # ... other fields ...
    }
    es_client.index(index="log_entries", document=doc)
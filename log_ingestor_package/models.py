# models.py
from sqlalchemy import Column, Integer, String, JSON
from log_ingestor_package.database import Base

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
    log_metadata = Column(JSON)  # Renamed from 'metadata' to 'log_metadata'

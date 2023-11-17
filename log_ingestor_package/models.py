from sqlalchemy import Column, Integer, String, DateTime, JSON
from .database import Base

class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(String)
    resourceId = Column(String)
    timestamp = Column(DateTime)
    traceId = Column(String)
    spanId = Column(String)
    commit = Column(String)
    log_metadata = Column(JSON)  # Renamed from 'metadata' to 'log_metadata'

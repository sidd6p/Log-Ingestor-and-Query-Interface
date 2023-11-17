# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class LogEntryBase(BaseModel):
    level: str
    message: str
    resourceId: str
    traceId: str
    spanId: str
    commit: str
    logs_metadata: Dict

class LogEntryCreate(LogEntryBase):
    pass

class LogEntry(LogEntryBase):
    timestamp: datetime

    class Config:
        orm_mode = True

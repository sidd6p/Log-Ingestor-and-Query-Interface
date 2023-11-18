# schemas.py
from pydantic import BaseModel
from typing import Dict


class LogEntryBase(BaseModel):
    level: str
    message: str
    resourceId: str
    traceId: str
    spanId: str
    commit: str
    # log_metadata: Dict


class LogEntry(LogEntryBase):
    timestamp: str

    class Config:
        orm_mode = True

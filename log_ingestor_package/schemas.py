from pydantic import BaseModel
from datetime import datetime

class LogData(BaseModel):
    level: str
    message: str
    resourceId: str
    timestamp: datetime
    traceId: str
    spanId: str
    commit: str
    log_metadata: dict  # Renamed from 'metadata' to 'log_metadata'

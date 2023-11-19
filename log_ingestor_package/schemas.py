# schemas.py
from pydantic import BaseModel, Field
from typing import Dict

class LogEntryBase(BaseModel):
    level: str
    message: str
    resourceId: str
    traceId: str
    spanId: str
    commit: str
    meta_data: Dict = Field(default=None, alias='metadata')  # Corrected to handle optional metadata

class LogEntry(LogEntryBase):
    timestamp: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # Allow population by both field name and alias

# schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Optional

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

class SearchCriteria(BaseModel):
    level: Optional[str] = None
    message: Optional[str] = None
    resource_id: Optional[str] = None
    timestamp: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    commit: Optional[str] = None
    parent_resource_id: Optional[str] = None
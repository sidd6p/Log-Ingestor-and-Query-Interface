from sqlalchemy.orm import Session
from . import models, schemas
import json

def create_log_entry(db: Session, log: schemas.LogData):
    db_log = models.LogEntry(
        level=log.level,
        message=log.message,
        resourceId=log.resourceId,
        timestamp=log.timestamp,
        traceId=log.traceId,
        spanId=log.spanId,
        commit=log.commit,
        log_metadata=json.dumps(log.log_metadata)  # Updated to 'log_metadata'
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

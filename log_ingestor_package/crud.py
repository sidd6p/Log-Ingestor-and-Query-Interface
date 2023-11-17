# crud.py
import json
from sqlalchemy.orm import Session
from log_ingestor_package import models, schemas

def create_log(db: Session, log: schemas.LogEntry):
    db_log = models.LogEntry(
        level=log.level,
        message=log.message,
        resourceId=log.resourceId,
        timestamp=str(log.timestamp),
        traceId=log.traceId,
        spanId=log.spanId,
        commit=log.commit,
        log_metadata=log.log_metadata # Updated to 'log_metadata'
        
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.LogEntry).offset(skip).limit(limit).all()



# crud.py
import json
from sqlalchemy.orm import Session
from log_ingestor_package import models, schemas


def create_log(db: Session, log: schemas.LogEntry):
    # Create and add log entry to PostgreSQL
    db_log = models.LogEntry(
        level=log.level,
        message=log.message,
        resourceId=log.resourceId,
        timestamp=str(log.timestamp),
        traceId=log.traceId,
        spanId=log.spanId,
        commit=log.commit,
        meta_data=log.meta_data,  # Added meta_data field
    )
    db.add(db_log)
    db.commit()

    # Index the same log entry in Elasticsearch
    models.index_log_entry(db_log)

    return db_log


def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.LogEntry).offset(skip).limit(limit).all()

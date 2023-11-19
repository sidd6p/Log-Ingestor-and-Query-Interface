from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from log_ingestor_package import database, rabbitmq_producer, models, config
from log_ingestor_package.schemas import LogEntry, SearchCriteria
from elasticsearch import Elasticsearch
from typing import Optional

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

# CORS Configuration (if needed)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

producer = rabbitmq_producer.RabbitMQProducer()


# Create a dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Elasticsearch index if not exists
models.create_elasticsearch_index()
es_client = Elasticsearch(config.settings.ELASTICSEARCH_URL)


# Testing endpoint to check if the server is running
@app.get("/health")
async def health_check():
    return {"status": "running"}


@app.post("/ingest")
async def ingest_log(log: LogEntry, db: database.SessionLocal = Depends(get_db)):
    # Publish log to RabbitMQ
    producer.publish_log(log)

    # Save log entry to PostgreSQL
    # db_log_entry = crud.create_log(db, log)

    return log


@app.get("/search")
def search_logs(
    criteria: SearchCriteria,
    db: database.SessionLocal = Depends(get_db),
):
    logs_query = db.query(models.LogEntry)
    
    if criteria.level:
        logs_query = logs_query.filter(models.LogEntry.level == criteria.level)
    if criteria.message:
        logs_query = logs_query.filter(models.LogEntry.message.contains(criteria.message))
    if criteria.resource_id:
        logs_query = logs_query.filter(models.LogEntry.resourceId == criteria.resource_id)
    if criteria.timestamp:
        logs_query = logs_query.filter(models.LogEntry.timestamp == criteria.timestamp)
    if criteria.trace_id:
        logs_query = logs_query.filter(models.LogEntry.traceId == criteria.trace_id)
    if criteria.span_id:
        logs_query = logs_query.filter(models.LogEntry.spanId == criteria.span_id)
    if criteria.commit:
        logs_query = logs_query.filter(models.LogEntry.commit == criteria.commit)

    if criteria.parent_resource_id:
            es_query = {
                "query": {
                    "nested": {
                        "path": "meta_data",
                        "query": {
                            "match": {
                                "meta_data.parentResourceId": criteria.parent_resource_id
                            }
                        }
                    }
                }
            }
            es_response = es_client.search(index="log_entries", body=es_query)
            log_ids = [hit["_id"] for hit in es_response["hits"]["hits"]]
            logs_query = logs_query.filter(models.LogEntry.id.in_(log_ids))

    logs = logs_query.all()
    return {"criteria": criteria, "logs": logs}
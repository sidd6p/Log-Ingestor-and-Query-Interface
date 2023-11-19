from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from log_ingestor_package import database, rabbitmq_producer, models, config, query_reader
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
    # return str(criteria.query)
    matches = query_reader.get_keys_values(criteria.query)
    logs_query = db.query(models.LogEntry)
    for key, value in matches:        
        if key == "level":
            logs_query = logs_query.filter(models.LogEntry.level == value)
        if key == "message":
            logs_query = logs_query.filter(models.LogEntry.message == value)
        if key == "resource_id":
            logs_query = logs_query.filter(models.LogEntry.resourceId == value)
        if key == "timestamp":
            logs_query = logs_query.filter(models.LogEntry.timestamp == value)
        if key == "trace_id":
            logs_query = logs_query.filter(models.LogEntry.traceId == value)
        if key == "span_id":
            logs_query = logs_query.filter(models.LogEntry.spanId == value)
        if key == "commit":
            logs_query = logs_query.filter(models.LogEntry.commit == value)

        if key == "metadata.parentResourceId":
                es_query = {
                    "query": {
                        "nested": {
                            "path": "meta_data",
                            "query": {
                                "match": {
                                    "meta_data.parentResourceId": value
                                }
                            }
                        }
                    }
                }
                es_response = es_client.search(index="log_entries", body=es_query)
                print(es_response["hits"]["hits"])
                log_ids = [hit["_source"]["id"] for hit in es_response["hits"]["hits"]]
                logs_query = logs_query.filter(models.LogEntry.id.in_(log_ids))

    logs = logs_query.all()
    print("##################################################")

    return logs
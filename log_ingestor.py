from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from log_ingestor_package import crud, database, rabbitmq_producer, models, config
from log_ingestor_package.schemas import LogEntry
from elasticsearch import Elasticsearch


app = FastAPI()

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
    # producer.publish_log(log)

    # Save log entry to PostgreSQL
    db_log_entry = crud.create_log(db, log)
    
    return {"status": "inserted"}


@app.get("/logs", response_model=List[LogEntry])
async def get_logs(
    skip: int = 0, limit: int = 100, db: database.SessionLocal = Depends(get_db)
):
    return crud.get_logs(db, skip=skip, limit=limit)


@app.get("/search")
async def search_logs(
    level: Optional[str] = Query(None),
    message: Optional[str] = Query(None),
    resourceId: Optional[str] = Query(None),
    timestamp: Optional[str] = Query(None),
    traceId: Optional[str] = Query(None),
    spanId: Optional[str] = Query(None),
    commit: Optional[str] = Query(None),
):
    query = {
        "bool": {
            "must": [],
            "filter": []
        }
    }

    if level:
        query["bool"]["filter"].append({"term": {"level": level}})
    if message:
        query["bool"]["must"].append({"match": {"message": message}})
    if resourceId:
        query["bool"]["filter"].append({"term": {"resourceId": resourceId}})
    if timestamp:
        query["bool"]["filter"].append({"range": {"timestamp": {"gte": timestamp}}})
    if traceId:
        query["bool"]["filter"].append({"term": {"traceId": traceId}})
    if spanId:
        query["bool"]["filter"].append({"term": {"spanId": spanId}})
    if commit:
        query["bool"]["filter"].append({"term": {"commit": commit}})

    response = es_client.search(
        index="log_entries",
        body={
            "query": query
        }
    )

    return response["hits"]["hits"]


if __name__ == "__main__":
    import uvicorn

    database.Base.metadata.create_all(bind=database.engine)
    uvicorn.run(app, host="0.0.0.0", port=3000)



from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from log_ingestor_package import crud, database, rabbitmq_producer, models, config
from log_ingestor_package.query_processor import parse_query, construct_es_query
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

    return db_log_entry


@app.get("/logs", response_model=List[LogEntry])
async def get_logs(
    skip: int = 0, limit: int = 99999999, db: database.SessionLocal = Depends(get_db)
):
    return crud.get_logs(db, skip=skip, limit=limit)


@app.post("/search")
async def search_logs(request: Request):
    body = await request.json()
    query_text = body.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Query text is required")

    parsed_params = parse_query(query_text)
    es_query = construct_es_query(parsed_params)
    response = es_client.search(index="log_entries", body={"query": es_query})

    return response["hits"]["hits"]


if __name__ == "__main__":
    import uvicorn

    database.Base.metadata.create_all(bind=database.engine)
    uvicorn.run(app, host="0.0.0.0", port=3000)

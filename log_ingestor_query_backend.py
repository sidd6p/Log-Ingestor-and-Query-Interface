from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from log_ingestor_package import database, rabbitmq_producer, models, config
from log_ingestor_package.query_processor import parse_query, construct_es_query
from log_ingestor_package.schemas import LogEntry
from elasticsearch import Elasticsearch

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
async def search_logs(request: Request):
    body = await request.json()
    query_text = body.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Query text is required")

    parsed_params = parse_query(query_text)
    es_query = construct_es_query(parsed_params)
    response = es_client.search(index="log_entries", body={"query": es_query})

    return response["hits"]["hits"]

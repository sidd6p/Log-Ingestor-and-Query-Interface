# log_ingestor.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from log_ingestor_package import crud, database, rabbitmq_producer
from log_ingestor_package.schemas import LogEntry


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

@app.post("/ingest", response_model=LogEntry)
async def ingest_log(log: LogEntry, db: database.SessionLocal = Depends(get_db)):
    # Publish log to RabbitMQ
    producer.publish_log(log)

    # Store log in the database
    return crud.create_log(db, log)

@app.get("/logs", response_model=List[LogEntry])
async def get_logs(skip: int = 0, limit: int = 10, db: database.SessionLocal = Depends(get_db)):
    return crud.get_logs(db, skip=skip, limit=limit)

if __name__ == "__main__":
    import uvicorn
    database.Base.metadata.create_all(bind=database.engine)
    uvicorn.run(app, host="0.0.0.0", port=3000)

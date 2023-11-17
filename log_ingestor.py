# log_ingestor.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from log_ingestor_package import crud, database, rabbitmq_producer
from log_ingestor_package.schemas import LogEntry  # Update this import statement

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

@app.post("/ingest", response_model=LogEntry)
async def ingest_log(log: LogEntry):
    # Publish log to RabbitMQ
    rabbitmq_producer.publish_log(log)

    # Store log in the database
    return crud.create_log(log)

@app.get("/logs", response_model=List[LogEntry])
async def get_logs(skip: int = 0, limit: int = 10):
    return crud.get_logs(skip=skip, limit=limit)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)

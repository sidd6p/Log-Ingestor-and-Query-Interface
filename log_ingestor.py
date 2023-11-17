from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI()

class LogData(BaseModel):
    level: str
    message: str
    resourceId: str
    timestamp: datetime
    traceId: str
    spanId: str
    commit: str
    metadata: dict

def process_log(log: LogData):
    # Simulate log processing
    print(f"Processing log: {log.model_dump_json()}")

@app.post("/ingest")
async def ingest_log(log: LogData, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_log, log)
    return {"status": "Log ingestion initiated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

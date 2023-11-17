from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from log_ingestor_package import crud, models, schemas
from log_ingestor_package.database import engine, SessionLocal 

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()  
    try:
        yield db
    finally:
        db.close()

def process_log(db: Session, log: schemas.LogData):
    return crud.create_log_entry(db, log)

@app.post("/ingest")
async def ingest_log(log: schemas.LogData, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(process_log, db, log)
    return {"status": "Log ingestion initiated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

from httpx import AsyncClient
from log_ingestor import app
import pytest
import json

@pytest.mark.asyncio
async def test_ingest_log():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ingest", json={
            "level": "error",
            "message": "Failed to connect to DB",
            "resourceId": "server-1234",
            "timestamp": "2023-09-15T08:00:00Z",
            "traceId": "abc-xyz-123",
            "spanId": "span-456",
            "commit": "5e5342f",
            "metadata": {"parentResourceId": "server-0987"}
        })
        assert response.status_code == 200
        assert response.json() == {"status": "Log ingestion initiated"}

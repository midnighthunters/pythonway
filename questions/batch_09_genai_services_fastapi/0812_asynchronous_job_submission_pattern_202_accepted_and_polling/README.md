# Q0812 · Asynchronous job submission pattern: 202 Accepted and polling

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code implementing an asynchronous job submission pattern in FastAPI: `POST /jobs` validates the request, enqueues work, and returns `202 Accepted` with a `job_id`, and `GET /jobs/{id}` returns execution status.

## Answer

For complex agentic workflows that take minutes (e.g. reconciling 10,000 trades or generating a 50-page investment prospectus), synchronous HTTP calls fail due to gateway timeouts.

Asynchronous Job Architecture:
- `POST /jobs`: Returns HTTP 202 Accepted with a unique `job_id` and status URL in the `Location` header.
- Background worker executes the workflow asynchronously.
- `GET /jobs/{job_id}`: Polled by the client to check status (`QUEUED` -> `PROCESSING` -> `COMPLETED` / `FAILED`).

```python
import uuid
from typing import Dict
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

app = FastAPI()

# In-memory job repository (in production: Redis or PostgreSQL)
JOB_DB: Dict[str, dict] = {}


@app.post("/jobs", status_code=status.HTTP_202_ACCEPTED)
def submit_job(payload: dict):
    job_id = f"job-{uuid.uuid4().hex[:8]}"
    JOB_DB[job_id] = {
        "id": job_id,
        "status": "QUEUED",
        "task": payload.get("task", "unnamed"),
        "result": None,
    }
    return {"job_id": job_id, "status": "QUEUED"}


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    if job_id not in JOB_DB:
        raise HTTPException(status_code=404, detail="Job not found")
    return JOB_DB[job_id]


client = TestClient(app)

# Submit job
post_resp = client.post("/jobs", json={"task": "Reconcile daily trades"})
assert post_resp.status_code == 202
job_id = post_resp.json()["job_id"]

# Poll job
get_resp = client.get(f"/jobs/{job_id}")
assert get_resp.status_code == 200
assert get_resp.json()["status"] == "QUEUED"
```

## Likely follow-ups

- Why should polling intervals use exponential backoff rather than aggressive fixed polling?
- When should push webhooks or WebSocket notifications replace client-side polling?

---

[← Q0811](../../batch_09_genai_services_fastapi/0811_managing_websocket_connection_pools_and_heartbeats/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0813 →](../../batch_09_genai_services_fastapi/0813_background_task_processing_with_fastapi_backgroundtasks/README.md)

# Q0813 · Background task processing with FastAPI BackgroundTasks

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Easy |

## Question

Write Python code demonstrating FastAPI's built-in `BackgroundTasks` for lightweight post-response tasks (e.g. logging audit records to disk or sending completion emails).

## Answer

`BackgroundTasks` runs tasks inside the same process after sending the HTTP response. It is ideal for lightweight operations that do not require external queue infrastructure (e.g. Celery or SQS).

```python
import time
from fastapi import BackgroundTasks, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
audit_trail = []


def record_audit_log(user_id: str, action: str):
    audit_trail.append({"user": user_id, "action": action, "timestamp": time.time()})


@app.post("/trade")
def execute_trade(payload: dict, background_tasks: BackgroundTasks):
    trade_id = payload.get("trade_id", "TRD-001")
    # Immediate response to client
    background_tasks.add_task(record_audit_log, user_id=payload.get("user", "trader1"), action=f"BOOKED_{trade_id}")
    return {"status": "Trade submitted", "trade_id": trade_id}


client = TestClient(app)
res = client.post("/trade", json={"trade_id": "TRD-999", "user": "alice"})
assert res.status_code == 200
assert len(audit_trail) == 1
assert audit_trail[0]["user"] == "alice"
assert audit_trail[0]["action"] == "BOOKED_TRD-999"
```

## Likely follow-ups

- What happens to pending `BackgroundTasks` if the container process crashes or restarts?
- When should you transition from `BackgroundTasks` to a distributed queue like Celery or ARQ?

---

[← Q0812](../../batch_09_genai_services_fastapi/0812_asynchronous_job_submission_pattern_202_accepted_and_polling/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0814 →](../../batch_09_genai_services_fastapi/0814_distributed_message_queues_celery_arq_and_redis_queue_for/README.md)

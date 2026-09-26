# Q0872 · Celery worker configuration for CPU-bound text splitting and embedding

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code configuring a Celery application for CPU-bound text chunking and embedding, specifying concurrency prefork settings and serializer formats.

## Answer

While LLM API calls are I/O-bound, PDF parsing, text normalization, and local ONNX embedding computation are CPU-intensive. Celery's `prefork` pool utilizes multiple CPU cores efficiently.

```python
# no-run
# Celery worker architecture configuration
from celery import Celery

celery_app = Celery("jpmc_embedding_worker")

celery_app.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/1",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Worker concurrency: 1 process per CPU core for CPU-bound tasks
    worker_concurrency=4,
    # Avoid memory leaks from native tokenizers by recycling after 500 tasks
    worker_max_tasks_per_child=500,
    # Prefetch 1 task at a time to prevent uneven distribution
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3)
def process_pdf_embeddings(self, document_id: str, text: str):
    # Simulated CPU-bound text splitting and vector generation
    chunks = [text[i : i + 500] for i in range(0, len(text), 500)]
    return {"doc_id": document_id, "chunk_count": len(chunks)}
```

## Likely follow-ups

- Why is `worker_prefetch_multiplier=1` essential for tasks with variable execution runtimes?
- How does `worker_max_tasks_per_child` resolve C-extension memory leaks (e.g. HuggingFace tokenizers)?

---

[← Q0871](../../batch_09_genai_services_fastapi/0871_arq_async_redis_job_queue_implementation_for_long_running/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0873 →](../../batch_09_genai_services_fastapi/0873_sqs_message_visibility_timeout_management_for_multi_minute/README.md)

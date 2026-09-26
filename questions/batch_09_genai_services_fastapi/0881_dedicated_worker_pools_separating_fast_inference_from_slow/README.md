# Q0881 · Dedicated worker pools: separating fast inference from slow scraping tasks

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Why should fast LLM inference tasks and slow document OCR/scraping tasks be routed to separate worker queues, and write Python code implementing queue routing logic.

## Answer

If fast interactive tasks (e.g. 500ms prompt completions) and slow heavyweight tasks (e.g. 10-minute PDF OCR or web scraping) share the same queue and worker pool, slow tasks will saturate all worker processes. Interactive user requests become head-of-line blocked behind long batch jobs.

Segregating tasks into dedicated queues (`queue_interactive` vs `queue_batch`) with independent worker pools guarantees interactive SLAs.

```python
from typing import Dict, List


class WorkerQueueRouter:
    def __init__(self):
        self.queues: Dict[str, List[dict]] = {
            "fast_interactive": [],
            "slow_batch": [],
        }

    def route_and_enqueue(self, task_type: str, payload: dict) -> str:
        if task_type in ["chat_completion", "single_tool_call", "sentiment_check"]:
            target_queue = "fast_interactive"
        elif task_type in ["pdf_ocr_extraction", "sec_filing_ingest", "web_crawl"]:
            target_queue = "slow_batch"
        else:
            target_queue = "fast_interactive"

        self.queues[target_queue].append(payload)
        return target_queue


router = WorkerQueueRouter()
q1 = router.route_and_enqueue("chat_completion", {"prompt": "Quick quote"})
q2 = router.route_and_enqueue("pdf_ocr_extraction", {"doc_url": "s3://docs/annual_report.pdf"})

assert q1 == "fast_interactive"
assert q2 == "slow_batch"
assert len(router.queues["fast_interactive"]) == 1
assert len(router.queues["slow_batch"]) == 1
```

## Likely follow-ups

- How does Celery route tasks via the `task_routes` setting?
- How do you autoscale fast worker pods independently of batch worker pods in Kubernetes?

---

[← Q0880](../../batch_09_genai_services_fastapi/0880_scheduling_recurring_batch_embedding_updates_with_celery/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0882 →](../../batch_09_genai_services_fastapi/0882_s3_large_payload_offloading_pattern_for_message_queues/README.md)

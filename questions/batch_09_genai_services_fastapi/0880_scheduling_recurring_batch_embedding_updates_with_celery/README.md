# Q0880 · Scheduling recurring batch embedding updates with Celery Beat

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Easy |

## Question

Explain how periodic scheduler systems (Celery Beat or Kubernetes CronJobs) orchestrate recurring vector index syncs, and write Python code evaluating cron schedule triggers.

## Answer

Financial research vector indexes must be refreshed on a strict schedule (e.g. every morning at 06:00 EST before market open) to ingest newly published SEC 8-K filings and sell-side equity research.

Celery Beat acts as a distributed scheduler, dispatching task messages to Redis/RabbitMQ queues at defined intervals.

```python
from datetime import datetime, timezone


class CronScheduleEvaluator:
    def __init__(self, target_hour_utc: int, target_minute_utc: int):
        self.target_hour = target_hour_utc
        self.target_minute = target_minute_utc
        self.last_triggered_date = None

    def should_trigger(self, current_dt: datetime) -> bool:
        if (
            current_dt.hour == self.target_hour
            and current_dt.minute == self.target_minute
        ):
            today = current_dt.date()
            if self.last_triggered_date != today:
                self.last_triggered_date = today
                return True
        return False


# Market open sync at 10:00 UTC
scheduler = CronScheduleEvaluator(target_hour_utc=10, target_minute_utc=0)

dt_not_yet = datetime(2026, 9, 26, 9, 59, tzinfo=timezone.utc)
assert scheduler.should_trigger(dt_not_yet) is False

dt_trigger = datetime(2026, 9, 26, 10, 0, tzinfo=timezone.utc)
assert scheduler.should_trigger(dt_trigger) is True

# Avoid double trigger in same minute
assert scheduler.should_trigger(dt_trigger) is False
```

## Likely follow-ups

- Why should Celery Beat only run as a single instance across an entire cluster (singleton)?
- How does Kubernetes CronJob offer an alternative to Celery Beat?

---

[← Q0879](../../batch_09_genai_services_fastapi/0879_handling_unhandled_worker_exceptions_and_capturing_crash/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0881 →](../../batch_09_genai_services_fastapi/0881_dedicated_worker_pools_separating_fast_inference_from_slow/README.md)

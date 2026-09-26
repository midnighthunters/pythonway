# Q0873 · SQS message visibility timeout management for multi-minute agent runs

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Hard |

## Question

Explain the AWS SQS Visibility Timeout mechanism during multi-minute agent execution runs, and write Python code implementing an asynchronous heartbeat extension loop.

## Answer

When a worker receives a message from AWS SQS, the message remains hidden from other workers for the duration of the **Visibility Timeout** (default: 30 seconds).

If a complex financial agent takes 3 minutes to execute multi-step research and tools, the visibility timeout will expire, causing a second worker to receive the message and start duplicate execution.

Solution: The worker must run a concurrent background task that calls `ChangeMessageVisibility` periodically to extend the lease until the run completes.

```python
import asyncio


class MockSQSClient:
    def __init__(self, initial_timeout: int = 10):
        self.visibility_timeout = initial_timeout
        self.extensions_count = 0

    async def change_message_visibility(self, receipt_handle: str, visibility_timeout: int) -> None:
        self.visibility_timeout = visibility_timeout
        self.extensions_count += 1


async def run_agent_with_visibility_heartbeat(
    sqs_client: MockSQSClient, receipt_handle: str, duration_sec: float
):
    agent_completed = False

    async def heartbeat():
        while not agent_completed:
            await asyncio.sleep(0.02)
            if not agent_completed:
                # Extend visibility timeout by 30 seconds
                await sqs_client.change_message_visibility(receipt_handle, 30)

    # Start heartbeat in background
    heartbeat_task = asyncio.create_task(heartbeat())

    # Simulate long-running agent execution
    await asyncio.sleep(duration_sec)
    agent_completed = True
    heartbeat_task.cancel()
    try:
        await heartbeat_task
    except asyncio.CancelledError:
        pass


async def main():
    sqs = MockSQSClient(initial_timeout=10)
    await run_agent_with_visibility_heartbeat(sqs, "handle_123", duration_sec=0.07)
    # Heartbeat must have fired at least twice
    assert sqs.extensions_count >= 2


asyncio.run(main())
```

## Likely follow-ups

- What is AWS SQS's maximum allowable visibility timeout (12 hours)?
- What happens if the worker process suffers a SIGKILL while the heartbeat is running?

---

[← Q0872](../../batch_09_genai_services_fastapi/0872_celery_worker_configuration_for_cpu_bound_text_splitting/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0874 →](../../batch_09_genai_services_fastapi/0874_job_status_tracking_state_machine_pending_running_success/README.md)

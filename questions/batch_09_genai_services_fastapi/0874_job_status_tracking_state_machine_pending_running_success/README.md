# Q0874 · Job status tracking state machine: PENDING, RUNNING, SUCCESS, FAILED

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Write Python code implementing a thread-safe finite state machine (FSM) to track asynchronous job transitions, preventing invalid status transitions (e.g. transitioning from SUCCESS to RUNNING).

## Answer

In distributed queue workers, concurrency races or delayed message retries can result in state corruption. An FSM validates that state transitions follow permitted lifecycles.

```python
from typing import Dict, Set


class InvalidStateTransitionError(Exception):
    pass


class JobStateMachine:
    VALID_TRANSITIONS: Dict[str, Set[str]] = {
        "PENDING": {"RUNNING", "CANCELLED"},
        "RUNNING": {"SUCCESS", "FAILED", "RETRYING"},
        "RETRYING": {"RUNNING", "FAILED"},
        "SUCCESS": set(),  # Terminal state
        "FAILED": set(),   # Terminal state
        "CANCELLED": set(),# Terminal state
    }

    def __init__(self, initial_state: str = "PENDING"):
        self.state = initial_state

    def transition_to(self, new_state: str) -> None:
        allowed = self.VALID_TRANSITIONS.get(self.state, set())
        if new_state not in allowed:
            raise InvalidStateTransitionError(
                f"Cannot transition from {self.state} to {new_state}"
            )
        self.state = new_state


job = JobStateMachine()
assert job.state == "PENDING"

# Valid transition: PENDING -> RUNNING
job.transition_to("RUNNING")
assert job.state == "RUNNING"

# Valid transition: RUNNING -> SUCCESS
job.transition_to("SUCCESS")
assert job.state == "SUCCESS"

# Invalid transition: SUCCESS -> RUNNING (Terminal state)
try:
    job.transition_to("RUNNING")
    assert False, "Should have failed invalid transition"
except InvalidStateTransitionError:
    pass
```

## Likely follow-ups

- How do you store and update job states in Redis Hashes atomically using Lua scripts?
- How do clients efficiently poll job status using HTTP 303 See Other / 200 OK patterns?

---

[← Q0873](../../batch_09_genai_services_fastapi/0873_sqs_message_visibility_timeout_management_for_multi_minute/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0875 →](../../batch_09_genai_services_fastapi/0875_real_time_progress_updates_via_redis_pubsub_during_batch/README.md)

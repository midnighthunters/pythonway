# Q0661 · A2A push notifications and webhook delivery

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

When an A2A task runs for 30 minutes, keeping an SSE connection open is fragile. How do A2A push notifications work, and write Python code that posts task completion to a webhook.

## Answer

For long-running tasks, callers provide a webhook endpoint during task submission (`push_notification_url: "https://caller.internal/webhooks/tasks"`). When the task finishes, the A2A server delivers a signed POST request.

```python
import hashlib
import hmac
import json
import time
from typing import Any, Dict


class A2AWebhookNotifier:
    def __init__(self, signing_secret: str):
        self.signing_secret = signing_secret.encode("utf-8")

    def create_notification_payload(self, task_id: str, status: str, result_summary: str) -> Dict[str, Any]:
        return {
            "task_id": task_id,
            "status": status,
            "summary": result_summary,
            "timestamp": int(time.time()),
        }

    def sign_payload(self, payload: Dict[str, Any]) -> str:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hmac.new(self.signing_secret, body, hashlib.sha256).hexdigest()

    def verify_signature(self, payload: Dict[str, Any], signature: str) -> bool:
        expected = self.sign_payload(payload)
        return hmac.compare_digest(expected, signature)


notifier = A2AWebhookNotifier("enterprise_shared_secret_key")
payload = notifier.create_notification_payload("tsk-99", "completed", "Batch settlement reconciliation finished.")
sig = notifier.sign_payload(payload)

assert notifier.verify_signature(payload, sig) is True
assert notifier.verify_signature(payload, "invalid_sig") is False
```

## Likely follow-ups

- Why is HMAC signing critical for webhook security?
- What retry policies should be applied if the caller's webhook returns HTTP 500?

---

[← Q0660](../../batch_07_mcp_a2a_skills_assistants/0660_parsing_a2a_streaming_event_frames_in_python/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0662 →](../../batch_07_mcp_a2a_skills_assistants/0662_a2a_task_cancellation_and_compensation/README.md)

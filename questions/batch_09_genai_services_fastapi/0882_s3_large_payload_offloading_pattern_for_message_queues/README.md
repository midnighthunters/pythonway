# Q0882 · S3 large payload offloading pattern for message queues (Claim-Check pattern)

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Asynchronous Queues | Medium |

## Question

Explain the Claim-Check pattern for message queues when job payloads exceed maximum message size (e.g. SQS 256 KB limit), and write Python code implementing automatic S3 offloading.

## Answer

AWS SQS and RabbitMQ enforce payload limits (typically 256 KB or 1 MB). Attempting to pass a 50MB PDF or 5,000-line financial transcript directly inside a queue message causes rejection or memory exhaustion.

In the **Claim-Check pattern**:
1. Payloads larger than a threshold (e.g. 64 KB) are uploaded to an S3 bucket or Azure Blob.
2. The message sent to the queue contains only metadata and the S3 URI pointer (the claim-check token).
3. The worker downloads the full payload from S3 upon dequeuing.

```python
from typing import Any, Dict, Tuple


class MockBlobStore:
    def __init__(self):
        self.blobs: Dict[str, str] = {}
        self.counter = 0

    def put_blob(self, data: str) -> str:
        self.counter += 1
        uri = f"s3://llm-suite-payloads/blob_{self.counter}.json"
        self.blobs[uri] = data
        return uri

    def get_blob(self, uri: str) -> str:
        return self.blobs[uri]


class ClaimCheckQueuePublisher:
    def __init__(self, blob_store: MockBlobStore, max_inline_chars: int = 100):
        self.blob_store = blob_store
        self.max_inline = max_inline_chars

    def prepare_message(self, data: str) -> Dict[str, Any]:
        if len(data) > self.max_inline:
            # Offload to blob store
            s3_uri = self.blob_store.put_blob(data)
            return {"claim_check": True, "payload_uri": s3_uri}
        else:
            return {"claim_check": False, "inline_payload": data}


def resolve_message(msg: Dict[str, Any], blob_store: MockBlobStore) -> str:
    if msg["claim_check"]:
        return blob_store.get_blob(msg["payload_uri"])
    return msg["inline_payload"]


blob = MockBlobStore()
pub = ClaimCheckQueuePublisher(blob, max_inline_chars=50)

# Small message: kept inline
small_msg = pub.prepare_message("Quick message")
assert small_msg["claim_check"] is False
assert resolve_message(small_msg, blob) == "Quick message"

# Large message: offloaded to S3
large_text = "Detailed Corporate Valuation Document... " * 10
large_msg = pub.prepare_message(large_text)
assert large_msg["claim_check"] is True
assert resolve_message(large_msg, blob) == large_text
```

## Likely follow-ups

- What lifecycle policy should be configured on the S3 payload bucket (e.g. 7-day auto-purge)?
- How does the AWS Extended Client Library for Python implement this automatically?

---

[← Q0881](../../batch_09_genai_services_fastapi/0881_dedicated_worker_pools_separating_fast_inference_from_slow/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0883 →](../../batch_09_genai_services_fastapi/0883_exactly_once_processing_versus_at_least_once_processing_in/README.md)

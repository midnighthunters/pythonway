# Q0734 · Checkpoint resumption for long-running batch inference

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Elastic Compute | Medium |

## Question

Write Python code for a batch inference worker that records progress to a state file and resumes execution seamlessly from the last processed record following an interruption.

## Answer

```python
from typing import Dict, List


class ResumableBatchWorker:
    def __init__(self, records: List[Dict[str, str]], processed_ids: set = None):
        self.records = records
        self.processed_ids = set(processed_ids or set())
        self.completed_results: Dict[str, str] = {}

    def run_batch(self, fail_at_id: str = None) -> None:
        for item in self.records:
            record_id = item["id"]
            if record_id in self.processed_ids:
                continue  # Skip already processed

            if fail_at_id and record_id == fail_at_id:
                raise InterruptedError(f"Spot instance evicted at record {record_id}")

            # Simulate processing
            self.completed_results[record_id] = f"Analyzed {item['text']}"
            self.processed_ids.add(record_id)


items = [{"id": f"rec_{i}", "text": f"Trade {i}"} for i in range(5)]
worker1 = ResumableBatchWorker(items)

# Process until eviction at rec_3
try:
    worker1.run_batch(fail_at_id="rec_3")
except InterruptedError:
    pass

assert worker1.processed_ids == {"rec_0", "rec_1", "rec_2"}
assert len(worker1.completed_results) == 3

# Resume with worker 2 using persisted processed_ids
worker2 = ResumableBatchWorker(items, processed_ids=worker1.processed_ids)
worker2.run_batch()
assert worker2.processed_ids == {"rec_0", "rec_1", "rec_2", "rec_3", "rec_4"}
assert "rec_4" in worker2.completed_results
```

## Likely follow-ups

- How does atomic checkpointing in S3 prevent corrupted state files?
- How do you handle poison-pill records that cause repeated worker crashes?

---

[← Q0733](../../batch_08_azure_openai_bedrock_cloud_ai/0733_spot_instances_for_batch_offline_llm_inference/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0735 →](../../batch_08_azure_openai_bedrock_cloud_ai/0735_multi_lora_adapter_serving_on_a_single_base_model/README.md)

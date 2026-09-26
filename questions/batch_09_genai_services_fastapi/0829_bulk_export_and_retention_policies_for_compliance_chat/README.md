# Q0829 · Bulk export and retention policies for compliance chat histories

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Write Python code implementing an automated data retention purger for NoSQL chat messages based on a strict 7-year financial record retention rule.

## Answer

Under SEC Rule 17a-4 and FINRA Rule 4511, customer communications and electronic trading interactions must be retained for at least 7 years in Write-Once-Read-Many (WORM) compliant storage, after which non-litigation data must be purged.

```python
from datetime import datetime, timezone, timedelta
from typing import Dict, List


class ComplianceAuditPurgeEngine:
    def __init__(self, retention_days: int = 7 * 365):
        self.retention_delta = timedelta(days=retention_days)

    def scan_and_partition_records(
        self, records: List[Dict], current_time: datetime
    ) -> Dict[str, List[Dict]]:
        retained = []
        purged = []
        legal_held = []

        cutoff_date = current_time - self.retention_delta

        for rec in records:
            if rec.get("legal_hold", False):
                legal_held.append(rec)
            elif rec["created_at"] < cutoff_date:
                purged.append(rec)
            else:
                retained.append(rec)

        return {"retained": retained, "purged": purged, "legal_held": legal_held}


engine = ComplianceAuditPurgeEngine(retention_days=7 * 365)
now = datetime.now(timezone.utc)
ten_years_ago = now - timedelta(days=10 * 365)
one_year_ago = now - timedelta(days=365)

dataset = [
    {"id": "doc1", "created_at": ten_years_ago, "legal_hold": False},
    {"id": "doc2", "created_at": ten_years_ago, "legal_hold": True},  # Under legal dispute
    {"id": "doc3", "created_at": one_year_ago, "legal_hold": False},
]

results = engine.scan_and_partition_records(dataset, now)
assert len(results["purged"]) == 1 and results["purged"][0]["id"] == "doc1"
assert len(results["legal_held"]) == 1 and results["legal_held"][0]["id"] == "doc2"
assert len(results["retained"]) == 1 and results["retained"][0]["id"] == "doc3"
```

## Likely follow-ups

- How does AWS DynamoDB TTL handle background deletion, and why does it not happen instantaneously?
- How do you guarantee immutability on S3 or Azure Blob storage using Object Lock?

---

[← Q0828](../../batch_09_genai_services_fastapi/0828_pii_encryption_at_rest_in_nosql_state_stores_with_envelope/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0830 →](../../batch_09_genai_services_fastapi/0830_read_consistency_models_in_nosql_state_stores_for_genai_apps/README.md)

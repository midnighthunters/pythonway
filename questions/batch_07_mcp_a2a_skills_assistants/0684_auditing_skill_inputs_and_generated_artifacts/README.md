# Q0684 · Auditing skill inputs and generated artifacts

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Agent skills | Medium |

## Question

Write Python code for an audit middleware that intercepts skill execution, captures input parameters, hashes generated output artifacts, and logs immutable audit records.

## Answer

```python
import hashlib
import json
import time
from typing import Any, Callable, Dict


class SkillAuditLogger:
    def __init__(self):
        self.audit_log = []

    def audit_skill_call(self, skill_name: str, user_id: str, inputs: Dict[str, Any], fn: Callable[[Dict[str, Any]], str]) -> str:
        start_time = time.time()
        output = fn(inputs)
        duration = round(time.time() - start_time, 4)

        output_hash = hashlib.sha256(output.encode("utf-8")).hexdigest()

        record = {
            "timestamp": int(start_time),
            "skill": skill_name,
            "user": user_id,
            "inputs": inputs,
            "duration_sec": duration,
            "output_sha256": output_hash,
        }
        self.audit_log.append(record)
        return output


auditor = SkillAuditLogger()
res = auditor.audit_skill_call(
    skill_name="export_tax_report",
    user_id="user_88",
    inputs={"year": 2026, "entity": "JPMC_UK"},
    fn=lambda inp: "Tax Liability: £0.00 (exempt)",
)

assert len(auditor.audit_log) == 1
assert auditor.audit_log[0]["skill"] == "export_tax_report"
assert len(auditor.audit_log[0]["output_sha256"]) == 64
```

## Likely follow-ups

- How does cryptographic artifact hashing assist during financial audits?
- How should PII in audited inputs be sanitized before persisting to log storage?

---

[← Q0683](../../batch_07_mcp_a2a_skills_assistants/0683_skill_versioning_deprecation_and_rollback_in_production/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0685 →](../../batch_07_mcp_a2a_skills_assistants/0685_implementing_a_dynamic_skill_registry_and_loader/README.md)

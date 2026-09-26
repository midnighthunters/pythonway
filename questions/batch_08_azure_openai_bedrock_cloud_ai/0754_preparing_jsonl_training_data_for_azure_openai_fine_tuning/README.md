# Q0754 · Preparing JSONL training data for Azure OpenAI fine-tuning

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Write Python code that validates a list of fine-tuning conversation records against Azure OpenAI requirements (checking roles, non-empty content, and serialization).

## Answer

```python
import json
from typing import Any, Dict, List, Tuple


class FineTuningDataValidator:
    VALID_ROLES = {"system", "user", "assistant"}

    @classmethod
    def validate_record(cls, record: Dict[str, Any]) -> Tuple[bool, str]:
        if "messages" not in record or not isinstance(record["messages"], list):
            return False, "Missing 'messages' list"

        messages = record["messages"]
        if len(messages) < 2:
            return False, "Must contain at least 2 messages"

        roles = [m.get("role") for m in messages]
        if not any(r == "assistant" for r in roles):
            return False, "Must contain at least one assistant message"

        for m in messages:
            if m.get("role") not in cls.VALID_ROLES:
                return False, f"Invalid role: {m.get('role')}"
            if not m.get("content", "").strip():
                return False, "Message content must not be empty"

        return True, "Valid"


valid_rec = {
    "messages": [
        {"role": "system", "content": "You are a JPMC trade format parser."},
        {"role": "user", "content": "Parse: BUY 100 AAPL @ 150"},
        {"role": "assistant", "content": '{"action": "BUY", "qty": 100, "sym": "AAPL", "px": 150.0}'},
    ]
}

ok, msg = FineTuningDataValidator.validate_record(valid_rec)
assert ok is True

bad_rec = {
    "messages": [
        {"role": "user", "content": "Only user message"},
        {"role": "user", "content": "Second user message"},
    ]
}
is_bad, err_msg = FineTuningDataValidator.validate_record(bad_rec)
assert is_bad is False
assert "assistant" in err_msg
```

## Likely follow-ups

- How does tokenizer token count per record affect fine-tuning training costs?
- What maximum token context window limits apply to fine-tuning on Azure OpenAI?

---

[← Q0753](../../batch_08_azure_openai_bedrock_cloud_ai/0753_fine_tuning_models_on_azure_openai_with_custom_enterprise/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0755 →](../../batch_08_azure_openai_bedrock_cloud_ai/0755_multi_tenant_quota_management_across_business_units/README.md)

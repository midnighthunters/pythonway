# Q0137 · Multi-label classification output

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Classification | Medium |

## Question

Model a multi-label tagger output that allows zero to three distinct labels from a fixed set, and rejects duplicates.

## Answer

```python
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

Tag = Literal["fraud_risk", "complaint", "vulnerable_customer", "sanctions", "none"]


class Tags(BaseModel):
    tags: list[Tag] = Field(max_length=3)

    @field_validator("tags")
    @classmethod
    def distinct_and_consistent(cls, v: list[str]) -> list[str]:
        if len(set(v)) != len(v):
            raise ValueError("duplicate tags")
        if "none" in v and len(v) > 1:
            raise ValueError("'none' cannot be combined with other tags")
        return v


assert Tags.model_validate({"tags": ["complaint", "vulnerable_customer"]}).tags == ["complaint", "vulnerable_customer"]
for bad in ({"tags": ["complaint", "complaint"]}, {"tags": ["none", "fraud"]}, {"tags": ["none", "sanctions"]},
            {"tags": ["fraud_risk", "complaint", "sanctions", "vulnerable_customer"]}):
    try:
        Tags.model_validate(bad)
        raise AssertionError(bad)
    except ValidationError:
        pass
```

For high-stakes tags (sanctions, vulnerability), evaluate per-label recall separately and consider one binary classifier per label, which is easier to calibrate and threshold than one multi-label prompt.

## Likely follow-ups

- Why might you prefer separate yes/no calls for rare but critical labels?

---

[← Q0136](../../batch_02_prompting_context_structured_output/0136_classification_prompt_with_label_definitions/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0138 →](../../batch_02_prompting_context_structured_output/0138_self_reported_confidence_pitfalls/README.md)

# Q0125 · Generate a JSON Schema from a Pydantic model

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Easy |

## Question

Show how to generate the JSON Schema for a structured-output request from a Pydantic model, and what to check in the generated schema.

## Answer

```python
from typing import Literal

from pydantic import BaseModel, Field


class Classification(BaseModel):
    """Routing decision for an employee request."""

    category: Literal["hr", "it", "finance", "other"] = Field(description="Team that should handle it")
    urgent: bool
    summary: str = Field(max_length=200, description="One-sentence summary")


schema = Classification.model_json_schema()
assert schema["type"] == "object"
assert schema["properties"]["category"]["enum"] == ["hr", "it", "finance", "other"]
assert set(schema["required"]) == {"category", "urgent", "summary"}
assert schema["description"] == "Routing decision for an employee request."
assert schema["properties"]["summary"]["maxLength"] == 200
```

Check that:
- Field descriptions are present. They act as prompts for the model.
- Enums come from `Literal` types, so labels are constrained.
- Nested models appear under `$defs` with `$ref`. Some providers require inlined or flattened schemas, or restrict `$ref`.
- The provider's strict mode rules are met (next question).

Generate the schema from the same model you validate with, so the contract lives in one place.

## Likely follow-ups

- Which JSON Schema keywords might a provider's strict mode not support?

---

[← Q0124](../../batch_02_prompting_context_structured_output/0124_extract_data_into_a_validated_pydantic_model/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0126 →](../../batch_02_prompting_context_structured_output/0126_make_a_schema_strict_for_providers/README.md)

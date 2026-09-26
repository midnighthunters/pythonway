# Q0187 · Tolerant parsing of older payloads

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Version 2 of an extraction model renamed `name` to `customer_name` and added `segment`. Write a Pydantic model that still reads v1 payloads (old field name, unknown legacy fields) while emitting v2.

## Answer

```python
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CustomerV2(BaseModel):
    model_config = ConfigDict(extra="ignore")

    customer_name: str = Field(validation_alias=AliasChoices("customer_name", "name"))
    segment: str = "unknown"
    schema_version: int = 2


v1 = CustomerV2.model_validate({"name": "Acme Ltd", "legacy_code": "X9"})
v2 = CustomerV2.model_validate({"customer_name": "Beta plc", "segment": "corporate", "schema_version": 2})
assert v1.model_dump() == {"customer_name": "Acme Ltd", "segment": "unknown", "schema_version": 2}
assert v2.segment == "corporate"
```

This is Postel's principle for data contracts: be liberal in what you read, strict in what you write. Use `extra="ignore"` for readers of stored or third-party data, but `extra="forbid"` when validating fresh model output, where unexpected fields mean the model went off-contract.

## Likely follow-ups

- Why use different `extra` settings for fresh model output and stored payloads?

---

[← Q0186](../../batch_02_prompting_context_structured_output/0186_schema_evolution_for_structured_outputs/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0188 →](../../batch_02_prompting_context_structured_output/0188_structured_outputs_versus_regex_post_processing/README.md)

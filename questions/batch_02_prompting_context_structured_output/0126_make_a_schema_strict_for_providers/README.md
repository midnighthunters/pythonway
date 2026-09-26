# Q0126 · Make a schema strict for providers

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Some providers' strict structured-output modes require every object to list all its properties in `required` and set `additionalProperties: false`. Optional fields must be expressed as nullable. Write a function that transforms a Pydantic-generated schema accordingly.

## Answer

```python
import copy
from typing import Optional

from pydantic import BaseModel


def make_strict(schema: dict) -> dict:
    s = copy.deepcopy(schema)

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "object" and "properties" in node:
                node["required"] = list(node["properties"])
                node["additionalProperties"] = False
                for prop in node["properties"].values():
                    prop.pop("default", None)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(s)
    return s


class Address(BaseModel):
    city: str
    postcode: Optional[str] = None


class Customer(BaseModel):
    name: str
    address: Address


strict = make_strict(Customer.model_json_schema())
addr = strict["$defs"]["Address"]
assert addr["required"] == ["city", "postcode"] and addr["additionalProperties"] is False
assert {"type": "null"} in addr["properties"]["postcode"]["anyOf"]
assert "default" not in addr["properties"]["postcode"]
assert strict["additionalProperties"] is False
```

`Optional[str] = None` already produces `anyOf: [string, null]`, so after marking it required, the model must send an explicit `null`. Your Pydantic model still accepts that. Check each provider's exact rules. They differ, and they change.

## Likely follow-ups

- What goes wrong if you drop an optional field entirely instead of making it nullable?

---

[← Q0125](../../batch_02_prompting_context_structured_output/0125_generate_a_json_schema_from_a_pydantic_model/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0127 →](../../batch_02_prompting_context_structured_output/0127_validate_and_retry_with_error_feedback/README.md)

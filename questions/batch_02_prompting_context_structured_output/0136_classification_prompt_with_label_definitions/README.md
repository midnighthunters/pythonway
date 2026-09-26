# Q0136 · Classification prompt with label definitions

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Classification | Easy |

## Question

Write a function that builds a classification prompt from a dictionary of label definitions, always includes an "other" label, delimits the input, and asks for JSON with a single label.

## Answer

```python
import json


def classification_prompt(labels: dict[str, str], text: str) -> str:
    labels = {**labels, "other": labels.get("other", "None of the above, or unclear")}
    defs = "\n".join(f"- {name}: {desc}" for name, desc in labels.items())
    return (
        "Classify the employee request into exactly one label.\n\n"
        f"Labels:\n{defs}\n\n"
        f"<request>\n{text}\n</request>\n\n"
        f'Respond with JSON only: {{"label": one of {json.dumps(sorted(labels))}}}'
    )


p = classification_prompt({"hr": "Leave, payroll, benefits", "it": "Laptops, access, software"},
                          "My VPN token expired")
assert "- it: Laptops, access, software" in p and "- other:" in p
assert '["hr", "it", "other"]' in p and "<request>\nMy VPN token expired\n</request>" in p
```

Clear, mutually exclusive definitions with boundary guidance ("password resets are it, not hr") improve accuracy more than extra examples. Pair this with a structured-output schema using an enum, so the label set is enforced rather than just requested.

## Likely follow-ups

- How do you handle requests that genuinely belong to two labels?

---

[← Q0135](../../batch_02_prompting_context_structured_output/0135_cross_field_validation_of_extracted_invoices/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0137 →](../../batch_02_prompting_context_structured_output/0137_multi_label_classification_output/README.md)

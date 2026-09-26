# Q0330 · Field-level extraction evaluation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Extraction evaluation | Medium |

## Question

Evaluate a document extractor field by field, with type-aware normalisation (amounts as Decimal, dates, case-insensitive strings), and report per-field accuracy and document-level exact match.

## Answer

```python
from datetime import date
from decimal import Decimal, InvalidOperation


def norm(field_type: str, v):
    if v is None:
        return None
    try:
        if field_type == "amount":
            return Decimal(str(v).replace(",", "").lstrip("£$€")).quantize(Decimal("0.01"))
        if field_type == "date":
            return date.fromisoformat(str(v))
    except (InvalidOperation, ValueError):
        return ("unparseable", v)
    return " ".join(str(v).lower().split())


def eval_extraction(preds: list[dict], golds: list[dict], schema: dict[str, str]) -> dict:
    per_field = {f: 0 for f in schema}
    doc_exact = 0
    for p, g in zip(preds, golds):
        ok_all = True
        for f, t in schema.items():
            ok = norm(t, p.get(f)) == norm(t, g.get(f))
            per_field[f] += ok
            ok_all &= ok
        doc_exact += ok_all
    n = len(golds)
    return {"per_field": {f: c / n for f, c in per_field.items()}, "doc_exact": doc_exact / n}


schema = {"vendor": "text", "amount": "amount", "due": "date"}
golds = [{"vendor": "Acme Ltd", "amount": "1,200.00", "due": "2026-10-01"},
         {"vendor": "Beta plc", "amount": "99.5", "due": None}]
preds = [{"vendor": "ACME  ltd", "amount": "£1200", "due": "2026-10-01"},
         {"vendor": "Beta plc", "amount": "95.50", "due": None}]
r = eval_extraction(preds, golds, schema)
assert r["per_field"] == {"vendor": 1.0, "amount": 0.5, "due": 1.0} and r["doc_exact"] == 0.5
```

Per-field results show where to focus (amounts here). Document-level exact match reflects how many documents could be processed with no human correction, which is often the business metric. Weight fields by business criticality.

## Likely follow-ups

- How would you evaluate fields that are lists (such as line items)?

---

[← Q0329](../../batch_04_llm_evaluation_observability/0329_jailbreak_success_rate_harness/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0331 →](../../batch_04_llm_evaluation_observability/0331_evaluating_summarisation/README.md)

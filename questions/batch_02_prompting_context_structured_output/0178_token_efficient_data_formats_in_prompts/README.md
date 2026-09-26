# Q0178 · Token-efficient data formats in prompts

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Cost optimisation | Easy |

## Question

Show how the same tabular data costs different amounts in pretty JSON, compact JSON and CSV, and explain when each format is the better choice.

## Answer

```python
import csv
import io
import json

rows = [{"date": f"2026-09-{d:02d}", "merchant": "Coffee Co", "amount": "3.50"} for d in range(1, 21)]
pretty = json.dumps(rows, indent=2)
compact = json.dumps(rows, separators=(",", ":"))
buf = io.StringIO()
writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
writer.writeheader()
writer.writerows(rows)
as_csv = buf.getvalue()

assert len(as_csv) < len(compact) < len(pretty)
assert len(as_csv) < 0.5 * len(pretty)
```

Character length is a proxy here. Token counts follow a similar pattern.

- CSV or markdown tables are best for uniform rows. Keys aren't repeated per row.
- Compact JSON suits nested or irregular data, or data the model must reproduce as JSON.
- Pretty JSON is readable for humans but wasteful in prompts.

Also drop columns the task doesn't need, round or format numbers consistently, and cap rows (with a count of omitted rows) or pre-aggregate in code.

## Likely follow-ups

- Why might CSV cause errors when fields contain commas or newlines, and how do you handle that?

---

[← Q0177](../../batch_02_prompting_context_structured_output/0177_prompt_compression/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0179 →](../../batch_02_prompting_context_structured_output/0179_render_tables_for_prompts_with_row_caps/README.md)

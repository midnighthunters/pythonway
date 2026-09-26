# Q0179 · Render tables for prompts with row caps

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Easy |

## Question

Write a markdown-table renderer for tool results that escapes pipe characters and newlines in cells, caps the number of rows, and states how many rows were omitted.

## Answer

```python
def markdown_table(rows: list[dict], columns: list[str], max_rows: int = 20) -> str:
    def cell(v) -> str:
        return str("" if v is None else v).replace("|", "\\|").replace("\n", " ")

    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    lines += ["| " + " | ".join(cell(r.get(c)) for c in columns) + " |" for r in rows[:max_rows]]
    if len(rows) > max_rows:
        lines.append(f"({len(rows) - max_rows} more rows not shown; {len(rows)} total)")
    return "\n".join(lines)


rows = [{"id": i, "memo": "refund | chargeback" if i == 0 else "ok\nline2", "amount": 10 * i} for i in range(25)]
t = markdown_table(rows, ["id", "memo", "amount"], max_rows=2)
assert t.splitlines()[2] == "| 0 | refund \\| chargeback | 0 |"
assert t.splitlines()[3] == "| 1 | ok line2 | 10 |"
assert t.endswith("(23 more rows not shown; 25 total)")
```

Stating the omitted count stops the model from claiming "there are only 2 transactions". For totals, compute aggregates in code and include them explicitly rather than asking the model to add up rows.

## Likely follow-ups

- Why should totals be computed in code rather than by the model?

---

[← Q0178](../../batch_02_prompting_context_structured_output/0178_token_efficient_data_formats_in_prompts/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0180 →](../../batch_02_prompting_context_structured_output/0180_inject_the_current_date_and_time_zone/README.md)

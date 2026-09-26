# Q0180 · Inject the current date and time zone

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Easy |

## Question

Models don't know today's date. Write a helper that renders the current date, weekday and UTC offset from a timezone-aware datetime, and say where in the prompt it should go.

## Answer

```python
from datetime import datetime, timedelta, timezone


def date_context(now: datetime) -> str:
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    off = now.strftime("%z")
    return f"Current date and time: {now:%Y-%m-%d %H:%M} ({now:%A}), time zone UTC{off[:3]}:{off[3:]}."


bst = timezone(timedelta(hours=1))
assert date_context(datetime(2026, 9, 26, 14, 5, tzinfo=bst)) == (
    "Current date and time: 2026-09-26 14:05 (Saturday), time zone UTC+01:00.")
try:
    date_context(datetime(2026, 9, 26))
    raise AssertionError
except ValueError:
    pass
```

Why it matters: "next Friday", "last quarter" and "overdue" all depend on today's date and the user's time zone. Use the user's time zone, not the server's.

Placement: put the date near the end of the prompt (with the user turn), not in the cached system prefix. A timestamp at the top changes on every request and destroys prompt-cache hits. For resolving relative dates, have the model output ISO dates and validate them in code, or resolve them with a date library.

## Likely follow-ups

- How should an agent resolve "the end of the month" for a user in New York when the server is in London?

---

[← Q0179](../../batch_02_prompting_context_structured_output/0179_render_tables_for_prompts_with_row_caps/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0181 →](../../batch_02_prompting_context_structured_output/0181_source_metadata_for_grounding/README.md)

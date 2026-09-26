# Q0145 · Schema context for text-to-SQL

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Text-to-SQL | Medium |

## Question

What schema information should you give an LLM for text-to-SQL, and write a function that renders a compact schema description from a database for the allowlisted tables.

## Answer

Give the model: table and column names with types, primary and foreign keys (join paths), short column descriptions and business definitions ("`net_flow` = inflow - outflow, in GBP"), enumerated values for coded columns, a few sample values, and a few verified example question→SQL pairs. Don't dump hundreds of tables. Retrieve the relevant ones per question.

```python
import sqlite3


def describe_schema(conn: sqlite3.Connection, tables: list[str], notes: dict[str, str] | None = None) -> str:
    notes = notes or {}
    known = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    lines = []
    for t in tables:
        if t not in known:
            raise ValueError(f"unknown table {t!r}")
        cols = conn.execute(f'PRAGMA table_info("{t}")').fetchall()
        col_desc = ", ".join(f"{c[1]} {c[2]}{' PK' if c[5] else ''}" for c in cols)
        lines.append(f"{t}({col_desc})" + (f"  -- {notes[t]}" if t in notes else ""))
    return "\n".join(lines)


conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE fx_rates(pair TEXT, rate_date TEXT, rate REAL, PRIMARY KEY(pair, rate_date))")
out = describe_schema(conn, ["fx_rates"], {"fx_rates": "daily closing rates, pair like GBPUSD"})
assert out == "fx_rates(pair TEXT PK, rate_date TEXT PK, rate REAL)  -- daily closing rates, pair like GBPUSD"
try:
    describe_schema(conn, ['x"; DROP TABLE fx_rates; --'])
    raise AssertionError
except ValueError:
    pass
```

Table names are checked against the catalogue before being interpolated into the PRAGMA, because identifiers can't be bound as parameters.

## Likely follow-ups

- How would you evaluate a text-to-SQL assistant (execution accuracy on a gold set)?

---

[← Q0144](../../batch_02_prompting_context_structured_output/0144_read_only_guardrails_for_text_to_sql/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0146 →](../../batch_02_prompting_context_structured_output/0146_the_sandwich_defence_and_its_limits/README.md)

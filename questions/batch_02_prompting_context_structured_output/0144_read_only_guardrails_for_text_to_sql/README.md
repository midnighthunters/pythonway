# Q0144 · Read-only guardrails for text-to-SQL

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Text-to-SQL | Hard |

## Question

An assistant generates SQL for analysts. Implement a guard with SQLite's authorizer that only permits reads from allowlisted tables, blocks writes and schema changes, runs one statement only, and caps rows. Explain the production equivalents.

## Answer

```python
import sqlite3


def run_readonly(conn: sqlite3.Connection, sql: str, allowed_tables: set[str], max_rows: int = 100):
    def authorizer(action, arg1, arg2, dbname, source):
        if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_FUNCTION):
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ:
            return sqlite3.SQLITE_OK if arg1 in allowed_tables else sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_DENY

    conn.set_authorizer(authorizer)
    try:
        return conn.execute(sql).fetchmany(max_rows)
    finally:
        conn.set_authorizer(None)


conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE accounts(id INTEGER, region TEXT, balance INTEGER);
CREATE TABLE salaries(emp TEXT, amount INTEGER);
INSERT INTO accounts VALUES (1, 'EMEA', 100), (2, 'EMEA', 250), (3, 'APAC', 75);
INSERT INTO salaries VALUES ('ceo', 999);
""")
allowed = {"accounts"}
assert run_readonly(conn, "SELECT region, SUM(balance) FROM accounts GROUP BY region ORDER BY region",
                    allowed) == [("APAC", 75), ("EMEA", 350)]
assert len(run_readonly(conn, "SELECT * FROM accounts", allowed, max_rows=2)) == 2
for attack in ("SELECT * FROM salaries", "DELETE FROM accounts", "DROP TABLE accounts",
               "SELECT 1; DROP TABLE accounts", "UPDATE accounts SET balance = 0"):
    try:
        run_readonly(conn, attack, allowed)
        raise AssertionError(attack)
    except sqlite3.Error:
        pass
assert conn.execute("SELECT COUNT(*) FROM accounts").fetchone() == (3,)
```

Production equivalents: a dedicated read-only database role with grants only on approved views, row-level security for entitlements, statement timeouts and cost limits, a read replica, parsing and validating the SQL with a real parser, and logging each query with the user identity. Never rely on the prompt ("only write SELECT statements") as the control.

## Likely follow-ups

- How do you enforce that a user only sees rows for their own business unit?

---

[← Q0143](../../batch_02_prompting_context_structured_output/0143_faithful_summaries_of_financial_documents/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0145 →](../../batch_02_prompting_context_structured_output/0145_schema_context_for_text_to_sql/README.md)

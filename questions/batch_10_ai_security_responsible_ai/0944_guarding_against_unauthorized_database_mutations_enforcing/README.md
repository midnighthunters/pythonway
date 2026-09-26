# Q0944 · Guarding against unauthorized database mutations: enforcing read-only SQL

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Write Python code configuring database connection pools and AST statement validation to guarantee that an LLM text-to-SQL agent can only execute read-only queries (`SELECT`).

## Answer

In Text-to-SQL workflows, an attacker can trick the model into generating `DROP TABLE accounts;` or `UPDATE balances SET amount = 9999999;`.

Defenses require:
1. Configuring the underlying database user account with strict `GRANT SELECT` read-only privileges.
2. Application-level SQL AST parsing to reject any non-SELECT statements.

```python
import re


def validate_read_only_sql(sql_query: str) -> bool:
    # 1. Strip comments (-- or /* */) to prevent comment hiding attacks
    cleaned = re.sub(r"--.*?(\n|$)", " ", sql_query)
    cleaned = re.sub(r"/\*.*?\*/", " ", cleaned, flags=re.DOTALL).strip()

    # 2. Reject queries containing multiple statements separated by semicolon
    statements = [s.strip() for s in cleaned.split(";") if s.strip()]
    if len(statements) > 1:
        return False  # Multi-statement injection attempt

    # 3. First token must be SELECT or WITH (for CTEs)
    tokens = cleaned.split()
    if not tokens:
        return False
    first_token = tokens[0].upper()
    if first_token not in ("SELECT", "WITH"):
        return False

    # 4. Must not contain mutating keywords
    FORBIDDEN_KEYWORDS = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT", "REVOKE"}
    words = set(re.findall(r"\b[A-Za-z]+\b", cleaned.upper()))
    if FORBIDDEN_KEYWORDS & words:
        return False

    return True


assert validate_read_only_sql("SELECT name, balance FROM accounts WHERE id = 42") is True
assert validate_read_only_sql("WITH high_val AS (SELECT * FROM trades) SELECT * FROM high_val") is True
assert validate_read_only_sql("DROP TABLE accounts") is False
assert validate_read_only_sql("SELECT * FROM accounts; DELETE FROM logs") is False
assert validate_read_only_sql("SELECT * FROM accounts -- UPDATE accounts SET balance = 0") is True
```

## Likely follow-ups

- Why is database-level permission enforcement (GRANT SELECT) more reliable than regex validation alone?
- How does SQLGlot provide comprehensive AST parsing across multiple SQL dialects?

---

[← Q0943](../../batch_10_ai_security_responsible_ai/0943_agent_credential_management_avoiding_long_lived_api_tokens/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0945 →](../../batch_10_ai_security_responsible_ai/0945_sql_query_ast_validation_and_blocking_ddl_dml_in_text_to/README.md)

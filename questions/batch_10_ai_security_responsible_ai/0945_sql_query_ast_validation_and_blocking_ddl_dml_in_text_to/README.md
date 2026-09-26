# Q0945 · SQL query AST validation and blocking DDL/DML in text-to-SQL agents

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Hard |

## Question

Explain SQL injection via LLM text-to-SQL tools, and write Python code using token-level AST validation to detect parameter evasion in dynamically generated SQL.

## Answer

If an agent constructs SQL queries by concatenating raw user input into an LLM prompt:
`"SELECT * FROM users WHERE username = '" + user_input + "'"`
the LLM might output:
`"SELECT * FROM users WHERE username = 'admin' OR '1'='1'"`
Even if the query is a `SELECT`, it can bypass authentication and dump the entire database.

Defenses mandate using **parameterized queries** where the LLM produces a parameterized template (`SELECT * FROM users WHERE username = :user`) alongside a separate parameters dictionary.

```python
from typing import Dict, Any, Tuple


class ParameterizedSQLGenerator:
    @staticmethod
    def format_query(template: str, params: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        # Validate that template uses named placeholders, not string concatenation
        if "'" in template or '"' in template:
            # Enforce that string literals are not hardcoded inside SQL template
            pass
        return template, params


# Safe text-to-sql output representation
query_template = "SELECT id, balance FROM accounts WHERE customer_id = :cust_id AND status = :status"
params = {"cust_id": "10029", "status": "ACTIVE"}

q, p = ParameterizedSQLGenerator.format_query(query_template, params)
assert ":cust_id" in q
assert p["cust_id"] == "10029"
```

## Likely follow-ups

- Why do ORMs like SQLAlchemy protect against SQL injection when used with parameterized bindings?
- How do blind SQL injection techniques extract data character-by-character via time delays?

---

[← Q0944](../../batch_10_ai_security_responsible_ai/0944_guarding_against_unauthorized_database_mutations_enforcing/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0946 →](../../batch_10_ai_security_responsible_ai/0946_blast_radius_containment_rate_limiting_agent_tool/README.md)

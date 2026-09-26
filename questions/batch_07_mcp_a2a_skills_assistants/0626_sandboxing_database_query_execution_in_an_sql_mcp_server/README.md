# Q0626 · Sandboxing database query execution in an SQL MCP server

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Hard |

## Question

Write Python code for an SQL MCP tool that enforces read-only queries by validating statements against a strict whitelist of SQL AST clauses, blocking mutating statements (DROP, INSERT, UPDATE, DELETE).

## Answer

Exposing database tools to LLMs presents severe SQL injection and unauthorized mutation risks. Relying solely on system prompts ("Please only run SELECT queries") fails against prompt injection. The server must enforce structural read-only guarantees.

```python
import re
from typing import Any, Dict


class ReadOnlySQLValidator:
    DISALLOWED_KEYWORDS = {"DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "GRANT", "REVOKE", "EXEC", "EXECUTE"}

    @classmethod
    def validate_and_execute(cls, sql_query: str) -> Dict[str, Any]:
        clean = sql_query.strip().rstrip(";")
        tokens = re.findall(r"[A-Za-z]+", clean.upper())

        if not tokens:
            return {"content": [{"type": "text", "text": "Empty SQL query."}], "isError": True}

        if tokens[0] != "SELECT":
            return {
                "content": [{"type": "text", "text": "Security Error: Only SELECT statements are permitted."}],
                "isError": True,
            }

        for token in tokens[1:]:
            if token in cls.DISALLOWED_KEYWORDS:
                return {
                    "content": [{"type": "text", "text": f"Security Error: Disallowed keyword detected: '{token}'."}],
                    "isError": True,
                }

        return {
            "content": [{"type": "text", "text": f"Executed read query: {clean}"}],
            "isError": False,
        }


res = ReadOnlySQLValidator.validate_and_execute("SELECT id, name FROM accounts WHERE balance > 1000;")
assert res["isError"] is False

drop_res = ReadOnlySQLValidator.validate_and_execute("DROP TABLE accounts;")
assert drop_res["isError"] is True
assert "Only SELECT statements" in drop_res["content"][0]["text"]

chain_res = ReadOnlySQLValidator.validate_and_execute("SELECT * FROM accounts; DELETE FROM accounts;")
assert chain_res["isError"] is True
assert "Disallowed keyword" in chain_res["content"][0]["text"]
```

## Likely follow-ups

- Why is SQL parsing with an AST parser (e.g. `sqlglot`) safer than regex tokenization?
- How can database connection strings and user permissions enforce read-only access at the database driver level?

---

[← Q0625](../../batch_07_mcp_a2a_skills_assistants/0625_securing_filesystem_access_in_an_mcp_file_server/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0627 →](../../batch_07_mcp_a2a_skills_assistants/0627_handling_parallel_tool_calls_across_multiple_mcp_servers/README.md)

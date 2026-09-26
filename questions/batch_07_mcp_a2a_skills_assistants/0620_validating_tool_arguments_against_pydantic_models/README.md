# Q0620 · Validating tool arguments against Pydantic models

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP tools | Medium |

## Question

Write Python code that uses Pydantic to validate arguments for an MCP `tools/call` invocation and automatically formats validation errors into an `isError: true` tool response.

## Answer

```python
from typing import Any, Dict
from pydantic import BaseModel, Field, ValidationError


class PortfolioRebalanceArgs(BaseModel):
    portfolio_id: str = Field(pattern=r"^PORT-[0-9]{4}$")
    target_allocations: Dict[str, float]
    dry_run: bool = True


def validate_and_execute_tool(raw_args: Dict[str, Any]) -> Dict[str, Any]:
    try:
        args = PortfolioRebalanceArgs.model_validate(raw_args)
    except ValidationError as exc:
        errors = [f"{e['loc'][0]}: {e['msg']}" for e in exc.errors()]
        return {
            "content": [{"type": "text", "text": f"Validation Error: {'; '.join(errors)}"}],
            "isError": True,
        }

    return {
        "content": [{"type": "text", "text": f"Rebalanced {args.portfolio_id} with dry_run={args.dry_run}"}],
        "isError": False,
    }


ok = validate_and_execute_tool({"portfolio_id": "PORT-1234", "target_allocations": {"AAPL": 0.5, "MSFT": 0.5}})
assert ok["isError"] is False
assert "Rebalanced PORT-1234" in ok["content"][0]["text"]

bad = validate_and_execute_tool({"portfolio_id": "BAD-ID", "target_allocations": {}})
assert bad["isError"] is True
assert "Validation Error" in bad["content"][0]["text"]
```

## Likely follow-ups

- How can Pydantic models be automatically converted into MCP `inputSchema` dictionaries?
- What are the performance implications of running Pydantic validation on thousands of tool calls?

---

[← Q0619](../../batch_07_mcp_a2a_skills_assistants/0619_reporting_tool_errors_iserror_flag_versus_json_rpc_error/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0621 →](../../batch_07_mcp_a2a_skills_assistants/0621_implementing_a_tool_execution_timeout/README.md)

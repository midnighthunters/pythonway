# Q0936 · Tool permission scopes and least privilege in agent tools

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Write Python code implementing Role-Based Access Control (RBAC) on agent tools, ensuring an agent cannot execute unauthorized tools based on the caller's JWT scope.

## Answer

An agent system may possess 20 tools (reading news, querying databases, executing trades, modifying client records). If a junior analyst interacts with the agent, the agent must be strictly restricted to the subset of tools authorized by the analyst's authentication claims.

```python
from typing import Dict, List, Set, Callable


class ToolRegistryRBAC:
    def __init__(self):
        self.tool_permissions: Dict[str, Set[str]] = {}
        self.tool_functions: Dict[str, Callable] = {}

    def register_tool(self, name: str, required_roles: List[str], func: Callable):
        self.tool_permissions[name] = set(required_roles)
        self.tool_functions[name] = func

    def execute_tool(self, name: str, user_roles: List[str], *args, **kwargs):
        if name not in self.tool_permissions:
            raise ValueError(f"Tool {name} does not exist.")

        required = self.tool_permissions[name]
        user_role_set = set(user_roles)

        if not (required & user_role_set):  # No intersection
            raise PermissionError(f"User with roles {user_roles} lacks required roles {list(required)} for {name}")

        return self.tool_functions[name](*args, **kwargs)


registry = ToolRegistryRBAC()
registry.register_tool("get_market_quote", ["ANALYST", "TRADER"], lambda ticker: f"{ticker}: $150")
registry.register_tool("execute_trade", ["TRADER"], lambda ticker, qty: f"Bought {qty} {ticker}")

# Analyst executes quote tool
assert registry.execute_tool("get_market_quote", ["ANALYST"], "AAPL") == "AAPL: $150"

# Analyst tries to execute trade tool
try:
    registry.execute_tool("execute_trade", ["ANALYST"], "AAPL", 100)
    assert False, "Should have raised PermissionError"
except PermissionError:
    pass

# Trader executes trade tool
assert registry.execute_tool("execute_trade", ["TRADER"], "AAPL", 100) == "Bought 100 AAPL"
```

## Likely follow-ups

- Why should tool authorizations be enforced by the backend runner rather than relying on system prompt instructions?
- How do OAuth2 scopes map to tool permissions in OpenAPI / MCP schemas?

---

[← Q0935](../../batch_10_ai_security_responsible_ai/0935_owasp_llm10_unbounded_consumption_and_denial_of_wallet/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0937 →](../../batch_10_ai_security_responsible_ai/0937_human_in_the_loop_approval_gates_for_sensitive_bank_actions/README.md)

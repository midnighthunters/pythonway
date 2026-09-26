# Q0640 · Access control on sensitive resources by URI pattern

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP resources | Hard |

## Question

Write Python code for an authorization interceptor that checks user role entitlements against URI regex patterns before fulfilling `resources/read` requests.

## Answer

Enterprise banks enforce strict segregation of duties (e.g. only compliance officers can view AML audit logs). An MCP server or gateway must evaluate access control policies before returning resource contents.

```python
import re
from typing import Any, Dict, List, Optional, Set


class ResourceAuthorizer:
    def __init__(self):
        self._role_policies: Dict[str, List[re.Pattern]] = {}

    def add_policy(self, role: str, pattern_str: str) -> None:
        if role not in self._role_policies:
            self._role_policies[role] = []
        self._role_policies[role].append(re.compile(pattern_str))

    def is_authorized(self, user_roles: Set[str], uri: str) -> bool:
        for role in user_roles:
            patterns = self._role_policies.get(role, [])
            for pat in patterns:
                if pat.match(uri):
                    return True
        return False


authorizer = ResourceAuthorizer()
authorizer.add_policy("trader", r"^market-data://.*")
authorizer.add_policy("compliance_officer", r"^audit://.*")
authorizer.add_policy("compliance_officer", r"^market-data://.*")

assert authorizer.is_authorized({"trader"}, "market-data://equity/AAPL") is True
assert authorizer.is_authorized({"trader"}, "audit://trades/2026-09-26") is False
assert authorizer.is_authorized({"compliance_officer"}, "audit://trades/2026-09-26") is True
```

## Likely follow-ups

- How should authorization failures be reported in the JSON-RPC response?
- How can OAuth 2.0 / Entra ID scopes be mapped to MCP resource URI patterns?

---

[← Q0639](../../batch_07_mcp_a2a_skills_assistants/0639_implementing_an_in_memory_resource_store_with_mime_types/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0641 →](../../batch_07_mcp_a2a_skills_assistants/0641_what_are_mcp_prompts_and_use_cases/README.md)

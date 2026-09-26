# Q0653 · A2A Agent Card specification and discovery

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Describe the structure of an A2A Agent Card and write Python code that serializes a valid Agent Card for a financial risk analysis agent.

## Answer

An Agent Card is a machine-readable JSON document published at a well-known endpoint (e.g. `/.well-known/agent-card.json`) that advertises an agent's identity, endpoints, capabilities, skills, and security requirements.

Key Fields:
- `id` & `name`: Unique identifier and human-readable name.
- `version`: Version of the agent implementation.
- `description`: Detailed description used by orchestrator LLMs for routing.
- `endpoints`: URLs for task creation, streaming, and status polling.
- `capabilities`: Supported features (e.g. `streaming: true`, `push_notifications: true`).
- `skills`: List of distinct capabilities, each with input/output schemas.
- `authentication`: Security schemes (e.g. OAuth 2.0 Bearer, mTLS).

```python
import json
from typing import Any, Dict


def build_risk_agent_card() -> Dict[str, Any]:
    return {
        "id": "agent-jpmc-risk-01",
        "name": "Market Risk Analysis Agent",
        "version": "1.0.0",
        "description": "Calculates Value at Risk (VaR), stress tests portfolios, and identifies concentration risk.",
        "endpoints": {
            "tasks": "https://risk.internal.bank/v1/tasks",
            "streaming": "https://risk.internal.bank/v1/tasks/{id}/events",
        },
        "capabilities": {
            "streaming": True,
            "push_notifications": True,
            "cancellation": True,
        },
        "skills": [
            {
                "id": "compute_var",
                "name": "Compute Value at Risk",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string"},
                        "confidence": {"type": "number", "default": 0.99},
                    },
                    "required": ["portfolio_id"],
                },
            }
        ],
        "authentication": {"type": "oauth2", "scopes": ["read:risk", "run:analysis"]},
    }


card = build_risk_agent_card()
assert card["id"] == "agent-jpmc-risk-01"
assert card["capabilities"]["streaming"] is True
assert card["skills"][0]["id"] == "compute_var"
```

## Likely follow-ups

- How does an orchestrator agent use the `description` in an Agent Card to decide routing?
- Why is versioning in Agent Cards essential when agents are upgraded independently?

---

[← Q0652](../../batch_07_mcp_a2a_skills_assistants/0652_mcp_versus_a2a_comparative_architectural_analysis/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0654 →](../../batch_07_mcp_a2a_skills_assistants/0654_validating_an_a2a_agent_card_against_json_schema/README.md)

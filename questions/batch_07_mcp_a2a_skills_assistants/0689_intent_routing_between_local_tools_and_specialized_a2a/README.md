# Q0689 · Intent routing between local tools and specialized A2A agents

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Hard |

## Question

Write Python code for an Assistant Router that inspects user queries and routes them to either immediate local MCP tools or long-running A2A remote agents.

## Answer

```python
from typing import Any, Dict


class AssistantIntentRouter:
    @staticmethod
    def classify_and_route(user_prompt: str) -> Dict[str, str]:
        prompt_lower = user_prompt.lower()

        if any(w in prompt_lower for w in ["deep analysis", "stress test", "reconcile all", "comprehensive audit"]):
            return {"target": "A2A_AGENT", "destination": "RiskOrchestratorAgent"}

        if any(w in prompt_lower for w in ["price of", "rate", "who is", "lookup", "balance"]):
            return {"target": "LOCAL_MCP", "destination": "market_data_server"}

        return {"target": "DIRECT_LLM", "destination": "default_model"}


r1 = AssistantIntentRouter.classify_and_route("What is the price of AAPL?")
assert r1["target"] == "LOCAL_MCP"

r2 = AssistantIntentRouter.classify_and_route("Run deep analysis and stress test on our Q3 book.")
assert r2["target"] == "A2A_AGENT"

r3 = AssistantIntentRouter.classify_and_route("Explain the concept of convexity.")
assert r3["target"] == "DIRECT_LLM"
```

## Likely follow-ups

- How do you handle hybrid queries that require a local tool lookup followed by an A2A delegation?
- What fallback occurs if the classifier incorrectly routes a complex query to a quick tool?

---

[← Q0688](../../batch_07_mcp_a2a_skills_assistants/0688_semantic_profile_store_for_user_preferences_and_entity/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0690 →](../../batch_07_mcp_a2a_skills_assistants/0690_calendar_and_meeting_management_via_personal_assistant/README.md)

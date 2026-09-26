# Q0823 · MongoDB document schema design for hierarchical agent traces

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Medium |

## Question

Design a MongoDB document schema in Python using Pydantic v2 to store nested agent execution traces, including tool calls, execution timestamps, token consumption, and intermediate thoughts.

## Answer

Unlike flat relational schemas, document databases like MongoDB or AWS DocumentDB excel at capturing polymorphic, deeply nested execution trees produced by multi-step agent reasoning (e.g. ReAct loops or Plan-and-Solve agents).

```python
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ToolExecutionTrace(BaseModel):
    tool_name: str
    tool_input: Dict[str, Any]
    tool_output: Optional[str] = None
    duration_ms: int
    error: Optional[str] = None


class AgentStepTrace(BaseModel):
    step_number: int
    thought: Optional[str] = None
    action_type: str  # "tool_call", "llm_generation", "final_response"
    tool_calls: List[ToolExecutionTrace] = Field(default_factory=list)
    tokens_used: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AgentRunDocument(BaseModel):
    run_id: str
    tenant_id: str
    user_id: str
    query: str
    final_output: Optional[str] = None
    steps: List[AgentStepTrace] = Field(default_factory=list)
    total_tokens: int = 0
    status: str = "COMPLETED"


# Verification
run = AgentRunDocument(
    run_id="run_991",
    tenant_id="dept_fx",
    user_id="trader_42",
    query="Fetch USD/EUR forward curves and summarize exposure",
)
step1 = AgentStepTrace(
    step_number=1,
    thought="Query market data API for USD/EUR forward points",
    action_type="tool_call",
    tool_calls=[
        ToolExecutionTrace(
            tool_name="get_forward_rates",
            tool_input={"pair": "USDEUR", "tenor": "3M"},
            tool_output="Forward point: +12.4 bps",
            duration_ms=45,
        )
    ],
    tokens_used=240,
)
run.steps.append(step1)
run.total_tokens = sum(s.tokens_used for s in run.steps)

doc_dict = run.model_dump()
assert doc_dict["run_id"] == "run_991"
assert len(doc_dict["steps"]) == 1
assert doc_dict["steps"][0]["tool_calls"][0]["tool_name"] == "get_forward_rates"
assert doc_dict["total_tokens"] == 240
```

## Likely follow-ups

- What is MongoDB's maximum document size limit (16MB), and how do you store traces exceeding this limit?
- How do you index fields inside arrays of subdocuments in MongoDB?

---

[← Q0822](../../batch_09_genai_services_fastapi/0822_cosmos_db_partition_key_strategies_for_enterprise_chat_apps/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0824 →](../../batch_09_genai_services_fastapi/0824_redis_vs_dynamodb_vs_postgresql_for_conversation_state/README.md)

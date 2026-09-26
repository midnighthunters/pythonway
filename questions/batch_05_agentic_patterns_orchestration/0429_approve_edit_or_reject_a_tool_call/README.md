# Q0429 · Approve, edit or reject a tool call

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Human-in-the-loop | Medium |

## Question

Extend human review so the reviewer can approve, edit the arguments (re-validated against the tool schema), or reject with a reason that goes back to the agent.

## Answer

```python
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class EmailArgs(BaseModel):
    to: str = Field(pattern=r"^[\w.+-]+@corp\.example$")
    subject: str = Field(max_length=120)
    body: str


class RefundArgs(BaseModel):
    order_id: str
    amount: Decimal = Field(gt=0, le=Decimal("500"))


SCHEMAS = {"send_email": EmailArgs, "issue_refund": RefundArgs}


def apply_review(call: dict, decision: Literal["approve", "edit", "reject"], edits: dict | None = None,
                 reason: str = "") -> dict:
    if decision == "reject":
        return {"action": "skip", "tool_message": f"The reviewer rejected {call['name']}: {reason}"}
    args = {**call["args"], **(edits or {})} if decision == "edit" else call["args"]
    try:
        validated = SCHEMAS[call["name"]].model_validate(args)
    except ValidationError as e:
        return {"action": "invalid_edit", "error": e.errors()[0]["msg"]}
    return {"action": "execute", "args": validated.model_dump()}


call = {"name": "issue_refund", "args": {"order_id": "O-1", "amount": "450"}}
assert apply_review(call, "approve")["args"]["amount"] == Decimal("450")
assert apply_review(call, "edit", {"amount": "120"})["args"]["amount"] == Decimal("120")
assert apply_review(call, "edit", {"amount": "5000"})["action"] == "invalid_edit"
assert apply_review(call, "reject", reason="duplicate claim")["tool_message"].endswith("duplicate claim")
```

Edits must pass the same validation as model-generated arguments, since human edits can be wrong too. Returning the rejection reason to the agent lets it adapt its plan ("the refund was rejected as a duplicate claim; tell the user"). Log the original arguments, the edits and who made them.

## Likely follow-ups

- Should edited calls be re-checked against authorisation rules as well?

---

[← Q0428](../../batch_05_agentic_patterns_orchestration/0428_human_approval_gate_for_side_effects/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0430 →](../../batch_05_agentic_patterns_orchestration/0430_risk_tiered_autonomy/README.md)

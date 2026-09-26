# Q0579 · StructuredTool with a Pydantic args schema

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain tools | Medium |

## Question

Build a tool from a function with an explicit Pydantic argument schema (patterns, bounds, field descriptions), and show that invalid arguments are rejected before the function runs.

## Answer

```python
from decimal import Decimal

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field, ValidationError


class RefundArgs(BaseModel):
    invoice_id: str = Field(pattern=r"^INV-\d{4,}$", description="Invoice id such as INV-0007")
    amount: Decimal = Field(gt=0, le=Decimal("500"), description="Refund amount in GBP, at most 500")


executed: list[str] = []


def issue_refund(invoice_id: str, amount: Decimal) -> str:
    executed.append(invoice_id)
    return f"Refund of {amount} GBP queued for {invoice_id}"


refund_tool = StructuredTool.from_function(func=issue_refund, name="issue_refund", args_schema=RefundArgs,
                                           description="Queue a refund for an invoice. Requires approval above 100 GBP.")
assert refund_tool.invoke({"invoice_id": "INV-0007", "amount": "45.00"}) == "Refund of 45.00 GBP queued for INV-0007"
for bad in ({"invoice_id": "7", "amount": "45"}, {"invoice_id": "INV-0007", "amount": "5000"}):
    try:
        refund_tool.invoke(bad)
        raise AssertionError(bad)
    except ValidationError:
        pass
assert executed == ["INV-0007"]
```

Schema validation stops malformed or out-of-range calls cheaply, and the field descriptions guide the model. Validation doesn't replace authorisation (can this user refund this invoice?) or approval rules. Those belong in the tool body or the dispatcher, driven by the authenticated context.

## Likely follow-ups

- Where would you put the approval requirement for refunds above 100 GBP?

---

[← Q0578](../../batch_06_langgraph_langchain/0578_define_tools_with_the_tool_decorator/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0580 →](../../batch_06_langgraph_langchain/0580_the_tool_calling_message_protocol/README.md)

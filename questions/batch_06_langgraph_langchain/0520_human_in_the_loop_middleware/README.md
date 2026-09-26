# Q0520 · Human-in-the-loop middleware

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangChain agents | Medium |

## Question

Configure `HumanInTheLoopMiddleware` so that an email-sending tool requires approval, and resume the paused agent with an approval decision.

## Answer

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


class FakeToolModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


sent: list[str] = []


@tool
def send_email(to: str, body: str) -> str:
    """Send an email to a colleague."""
    sent.append(to)
    return f"sent to {to}"


model = FakeToolModel(messages=iter([
    AIMessage(content="", tool_calls=[{"name": "send_email", "args": {"to": "tom@corp.example", "body": "Agenda"}, "id": "c1"}]),
    AIMessage(content="Email sent to Tom."),
]))
agent = create_agent(model, tools=[send_email], checkpointer=InMemorySaver(),
                     middleware=[HumanInTheLoopMiddleware(interrupt_on={"send_email": True})])
cfg = {"configurable": {"thread_id": "email-1"}}
paused = agent.invoke({"messages": [HumanMessage("Email Tom the agenda")]}, cfg)
request = paused["__interrupt__"][0].value
assert request["action_requests"][0]["name"] == "send_email" and sent == []
assert "approve" in request["review_configs"][0]["allowed_decisions"]
done = agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}), cfg)
assert sent == ["tom@corp.example"] and done["messages"][-1].content == "Email sent to Tom."
```

Nothing is sent until the reviewer approves. The interrupt payload lists each pending action and the decisions allowed (approve, edit, reject, respond), which is what a review UI renders. Keep the tool list for `interrupt_on` in configuration owned by risk, and log every decision with the reviewer's identity.

## Likely follow-ups

- How would the UI show the reviewer exactly what will be sent?

---

[← Q0519](../../batch_06_langgraph_langchain/0519_agent_middleware_in_langchain_1_x/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0521 →](../../batch_06_langgraph_langchain/0521_checkpointers_and_threads/README.md)

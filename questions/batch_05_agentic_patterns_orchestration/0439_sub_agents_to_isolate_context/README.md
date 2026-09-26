# Q0439 · Sub-agents to isolate context

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Context engineering | Medium |

## Question

Show how delegating a noisy sub-task to a sub-agent keeps the parent's context small: the sub-agent may make many tool calls, but only a concise result returns to the parent.

## Answer

```python
from typing import Callable


def research_subagent(question: str, search: Callable[[str], list[str]], max_calls: int = 5) -> dict:
    notes, calls = [], 0
    for q in [question, question + " exceptions", question + " effective date"][:max_calls]:
        calls += 1
        notes.extend(search(q))
    unique = list(dict.fromkeys(notes))
    return {"summary": "; ".join(unique[:3]), "sources": len(unique), "tool_calls": calls}


def parent_agent(task: str, search: Callable[[str], list[str]]) -> list[dict]:
    context = [{"role": "user", "content": task}]
    result = research_subagent("UK hotel cap", search)
    context.append({"role": "tool", "name": "research", "content": result["summary"]})
    return context


corpus = {"UK hotel cap": ["London cap 180 GBP [pol-7]", "Rest of UK 120 GBP [pol-7]"],
          "UK hotel cap exceptions": ["Director approval above cap [pol-7]"],
          "UK hotel cap effective date": ["Effective 2026-04-01 [pol-7]"]}
ctx = parent_agent("Draft a travel note", lambda q: corpus.get(q, []))
assert len(ctx) == 2 and ctx[1]["content"].startswith("London cap 180 GBP")
assert research_subagent("UK hotel cap", lambda q: corpus.get(q, []))["tool_calls"] == 3
```

Three searches and four raw results collapse into one line in the parent's context. This improves focus and cost, and keeps parallel sub-agents independent. The risk is information loss in the summary, so return structured results with citations, and let the parent ask follow-up questions.

## Likely follow-ups

- When would you pass the sub-agent's full transcript back instead?

---

[← Q0438](../../batch_05_agentic_patterns_orchestration/0438_summarise_tool_outputs_between_steps/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0440 →](../../batch_05_agentic_patterns_orchestration/0440_token_and_cost_budget_manager/README.md)

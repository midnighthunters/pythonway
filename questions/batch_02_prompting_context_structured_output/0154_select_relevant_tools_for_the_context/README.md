# Q0154 · Select relevant tools for the context

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Tool use | Medium |

## Question

An agent platform has 150 tools, and loading all of them wastes context and hurts selection. Implement a simple tool retriever that ranks tools by keyword overlap with the query, always includes pinned tools, and returns the top k.

## Answer

```python
import re

STOP = {"the", "a", "an", "to", "for", "of", "my", "me", "is", "what", "and", "in", "on"}


def tokens(text: str) -> set[str]:
    return {w.rstrip("s") for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP}


def select_tools(query: str, tools: list[dict], k: int, pinned: set[str] = frozenset()) -> list[str]:
    q = tokens(query)
    scored = []
    for t in tools:
        if t["name"] in pinned:
            continue
        overlap = len(q & tokens(t["name"].replace("_", " ") + " " + t["description"]))
        scored.append((-overlap, t["name"]))
    ranked = [name for score, name in sorted(scored) if score < 0]
    return sorted(pinned) + ranked[:max(0, k - len(pinned))]


tools = [
    {"name": "get_account_balance", "description": "Current balance for an account"},
    {"name": "list_transactions", "description": "Transactions for an account in a date range"},
    {"name": "book_meeting_room", "description": "Reserve a meeting room"},
    {"name": "search_policies", "description": "Search internal HR and travel policies"},
]
assert select_tools("What is the balance of my savings account?", tools, k=2) == [
    "get_account_balance", "list_transactions"]
assert select_tools("travel policy for trains", tools, k=2, pinned={"ask_user"}) == ["ask_user", "search_policies"]
assert select_tools("hello", tools, k=3) == []
```

Production versions embed the tool descriptions and use vector search, sometimes with an LLM re-ranking step. Log misses (the model needed a tool that wasn't loaded) and give the agent a `find_tools` meta-tool so it can pull in more on demand.

## Likely follow-ups

- What are the risks of dynamically changing the tool list mid-conversation (prompt caching, model confusion)?

---

[← Q0153](../../batch_02_prompting_context_structured_output/0153_writing_good_tool_descriptions/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0155 →](../../batch_02_prompting_context_structured_output/0155_assemble_the_system_prompt_per_user_role/README.md)

# Q0155 · Assemble the system prompt per user role

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Context engineering | Medium |

## Question

Write a function that builds the system prompt from a base section, role-specific instructions, and only the tools that role is allowed. Unknown roles must fail closed.

## Answer

```python
BASE = "You are the LLM Suite assistant. Answer from provided sources and cite them."
ROLE_RULES = {
    "analyst": "You may explain methodologies. Do not provide client-identifying details.",
    "hr_partner": "You may discuss HR policy cases. Follow data-minimisation rules.",
}
ROLE_TOOLS = {
    "analyst": ["search_research", "run_readonly_sql"],
    "hr_partner": ["search_policies"],
}
TOOL_DOCS = {
    "search_research": "search_research(query): internal research notes",
    "run_readonly_sql": "run_readonly_sql(sql): read-only analytics warehouse",
    "search_policies": "search_policies(query): HR policies",
}


def build_system_prompt(role: str) -> tuple[str, list[str]]:
    if role not in ROLE_RULES:
        raise PermissionError(f"no assistant configuration for role {role!r}")
    tools = ROLE_TOOLS[role]
    text = "\n\n".join([BASE, ROLE_RULES[role], "Tools:\n" + "\n".join(f"- {TOOL_DOCS[t]}" for t in tools)])
    return text, tools


prompt, tools = build_system_prompt("hr_partner")
assert tools == ["search_policies"] and "run_readonly_sql" not in prompt
try:
    build_system_prompt("intern")
    raise AssertionError
except PermissionError:
    pass
```

The prompt only describes permissions. The real enforcement is that the tool dispatcher, for this session, only accepts the tools returned here, and each tool re-checks the user's entitlements server-side.

## Likely follow-ups

- Why must the tool dispatcher enforce the same list rather than trusting the prompt?

---

[← Q0154](../../batch_02_prompting_context_structured_output/0154_select_relevant_tools_for_the_context/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0156 →](../../batch_02_prompting_context_structured_output/0156_context_distraction_and_poisoning/README.md)

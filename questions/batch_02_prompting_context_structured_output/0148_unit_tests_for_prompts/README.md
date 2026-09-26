# Q0148 · Unit tests for prompts

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt testing | Medium |

## Question

Write "lint" checks that run in CI on every rendered prompt: no unfilled placeholders, the required safety clause is present, the schema is embedded, and it's under a token budget.

## Answer

```python
import re


def lint_prompt(rendered: str, *, required_phrases: list[str], max_tokens: int,
                count_tokens=lambda s: len(s) // 4) -> list[str]:
    problems = []
    if re.search(r"\$\{?\w+\}?|\{\{\s*\w+\s*\}\}", rendered):
        problems.append("unfilled placeholder")
    for phrase in required_phrases:
        if phrase.lower() not in rendered.lower():
            problems.append(f"missing required phrase: {phrase!r}")
    if count_tokens(rendered) > max_tokens:
        problems.append(f"over budget: {count_tokens(rendered)} > {max_tokens} tokens")
    if re.search(r"(api[_-]?key|password)\s*[:=]\s*\S+", rendered, re.I):
        problems.append("possible secret in prompt")
    return problems


good = "You answer from sources only. If unsure, say you don't know.\nSchema: {...}\nQuestion: Is travel allowed?"
assert lint_prompt(good, required_phrases=["sources only", "Schema:"], max_tokens=100) == []
bad = "Question: $question\napi_key=sk-123 " + "x" * 800
issues = lint_prompt(bad, required_phrases=["sources only"], max_tokens=100)
assert issues[0] == "unfilled placeholder" and any("secret" in i for i in issues) and len(issues) == 4
```

These are cheap, deterministic checks that belong next to the behavioural evaluations. They catch the dumb bugs (template regressions, leaked credentials, bloated prompts) before any model is called.

## Likely follow-ups

- What other deterministic checks would you add?

---

[← Q0147](../../batch_02_prompting_context_structured_output/0147_automatic_prompt_optimisation_with_an_eval_loop/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0149 →](../../batch_02_prompting_context_structured_output/0149_snapshot_testing_rendered_prompts/README.md)

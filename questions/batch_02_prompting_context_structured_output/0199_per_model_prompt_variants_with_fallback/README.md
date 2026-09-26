# Q0199 · Per-model prompt variants with fallback

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Model-agnostic design | Medium |

## Question

On a model-agnostic platform, the same logical prompt sometimes needs model-family-specific wording. Implement a variant registry that picks a family-specific version and falls back to a default.

## Answer

```python
class PromptVariants:
    def __init__(self) -> None:
        self._variants: dict[tuple[str, str], str] = {}

    def add(self, name: str, family: str, text: str) -> None:
        self._variants[(name, family)] = text

    def get(self, name: str, model_id: str, families: dict[str, str]) -> tuple[str, str]:
        family = next((fam for prefix, fam in families.items() if model_id.startswith(prefix)), "default")
        if (name, family) in self._variants:
            return self._variants[(name, family)], family
        if (name, "default") in self._variants:
            return self._variants[(name, "default")], "default"
        raise KeyError(f"no variant of {name!r} for {model_id!r}")


FAMILIES = {"gpt-": "openai", "anthropic.claude": "claude", "claude-": "claude"}
pv = PromptVariants()
pv.add("extract", "default", "Extract the fields as JSON.")
pv.add("extract", "claude", "Extract the fields. Put the JSON inside <json> tags.")
assert pv.get("extract", "anthropic.claude-x-2026", FAMILIES)[1] == "claude"
assert pv.get("extract", "gpt-x-mini", FAMILIES) == ("Extract the fields as JSON.", "default")
try:
    pv.get("summarise", "gpt-x", FAMILIES)
    raise AssertionError
except KeyError:
    pass
```

The model id strings are illustrative. Keep variants to the minimum. Most differences are better handled by the provider adapter (formats, structured-output features), and each variant needs its own evaluation run. Record which variant was used on every call.

## Likely follow-ups

- When would you rather fix a difference in the provider adapter than in the prompt?

---

[← Q0198](../../batch_02_prompting_context_structured_output/0198_prompt_debugging_workflow/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0200 →](../../batch_02_prompting_context_structured_output/0200_design_the_prompt_stack_for_an_llm_suite_assistant/README.md)

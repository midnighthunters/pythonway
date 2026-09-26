# Q0103 · Render versioned prompt templates safely

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt management | Medium |

## Question

Implement a prompt template class that knows its name and version, lists its variables, and refuses to render with missing or unexpected variables. Use it without f-strings on user input.

## Answer

Why it matters here: a silent empty variable (for example missing retrieved context) produces confident nonsense. Failing loudly makes prompt bugs visible in tests.

```python
import string


class PromptTemplate:
    def __init__(self, name: str, version: str, text: str) -> None:
        self.name, self.version = name, version
        self._t = string.Template(text)
        if not self._t.is_valid():
            raise ValueError("invalid placeholder syntax")
        self.variables = set(self._t.get_identifiers())

    def render(self, **values: str) -> str:
        missing = self.variables - values.keys()
        extra = values.keys() - self.variables
        if missing or extra:
            raise KeyError(f"{self.name}@{self.version}: missing={sorted(missing)} extra={sorted(extra)}")
        return self._t.substitute({k: str(v) for k, v in values.items()})


t = PromptTemplate("policy_qa", "1.2.0", "Sources:\n$sources\n\nQuestion: $question")
assert t.variables == {"sources", "question"}
out = t.render(sources="[1] Travel policy", question="Is ${price} {x} allowed?")
assert out.endswith("Question: Is ${price} {x} allowed?")
for bad in ({"sources": "x"}, {"sources": "x", "question": "y", "user_id": "z"}):
    try:
        t.render(**bad)
        raise AssertionError
    except KeyError:
        pass
```

`string.Template` doesn't re-interpret `$` or `{}` inside substituted values, so user text is inserted literally. Jinja2 with autoescape off and a sandboxed environment is the other common choice. Just avoid `str.format` with templates users can influence.

## Likely follow-ups

- Where would you store prompts: in code, config or a prompt registry?

---

[← Q0102](../../batch_02_prompting_context_structured_output/0102_zero_shot_few_shot_and_instruction_prompts/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0104 →](../../batch_02_prompting_context_structured_output/0104_prompt_registry_with_versions_and_rollback/README.md)

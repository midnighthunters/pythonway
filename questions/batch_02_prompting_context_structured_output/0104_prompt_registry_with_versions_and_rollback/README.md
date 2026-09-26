# Q0104 · Prompt registry with versions and rollback

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt management | Medium |

## Question

Implement an in-memory prompt registry: register immutable versions, content-hash each version, activate one version per prompt name, roll back to the previous active version, and record the hash so logs can prove which prompt produced a response.

## Answer

```python
import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class PromptVersion:
    name: str
    version: str
    text: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode()).hexdigest()[:12]


class PromptRegistry:
    def __init__(self) -> None:
        self._versions: dict[tuple[str, str], PromptVersion] = {}
        self._history: dict[str, list[str]] = {}

    def register(self, name: str, version: str, text: str) -> PromptVersion:
        key = (name, version)
        if key in self._versions:
            if self._versions[key].text != text:
                raise ValueError(f"{name}@{version} already exists with different content")
            return self._versions[key]
        pv = PromptVersion(name, version, text)
        self._versions[key] = pv
        return pv

    def activate(self, name: str, version: str) -> None:
        if (name, version) not in self._versions:
            raise KeyError(f"unknown version {name}@{version}")
        self._history.setdefault(name, []).append(version)

    def active(self, name: str) -> PromptVersion:
        return self._versions[(name, self._history[name][-1])]

    def rollback(self, name: str) -> PromptVersion:
        if len(self._history.get(name, [])) < 2:
            raise ValueError("nothing to roll back to")
        self._history[name].pop()
        return self.active(name)


reg = PromptRegistry()
reg.register("summarise", "1.0", "Summarise: $text")
reg.register("summarise", "1.1", "Summarise in 3 bullets: $text")
reg.activate("summarise", "1.0")
reg.activate("summarise", "1.1")
assert reg.active("summarise").version == "1.1"
assert reg.rollback("summarise").version == "1.0"
try:
    reg.register("summarise", "1.0", "changed!")
    raise AssertionError
except ValueError:
    pass
assert len(reg.active("summarise").sha256) == 12
```

In production, this lives in a database or config repo with approvals, and changes go through the same review, evaluation gates and audit trail as code. LangSmith and similar tools offer hosted prompt hubs with versioning.

## Likely follow-ups

- Why must published versions be immutable?

---

[← Q0103](../../batch_02_prompting_context_structured_output/0103_render_versioned_prompt_templates_safely/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0105 →](../../batch_02_prompting_context_structured_output/0105_delimit_untrusted_content_in_prompts/README.md)

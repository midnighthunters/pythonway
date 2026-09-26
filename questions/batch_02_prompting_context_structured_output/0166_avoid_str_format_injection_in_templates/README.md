# Q0166 · Avoid str.format injection in templates

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt safety | Medium |

## Question

Show two bugs with `str.format` in prompt code: a user-controlled format string leaking object attributes, and literal JSON braces in a template crashing it. Then show safe alternatives.

## Answer

```python
import string


class Settings:
    API_KEY = "sk-test-not-real"


user_template = "Hello {cfg.__class__.API_KEY}"
assert user_template.format(cfg=Settings()) == "Hello sk-test-not-real"

template_with_json = 'Return JSON like {"label": "..."} for: {text}'
try:
    template_with_json.format(text="hi")
    raise AssertionError
except KeyError:
    pass

safe = string.Template('Return JSON like {"label": "..."} for: $text')
assert safe.substitute(text="{cfg.__class__}") == 'Return JSON like {"label": "..."} for: {cfg.__class__}'
assert 'Return JSON like {{"label": "..."}} for: {text}'.format(text="hi") == 'Return JSON like {"label": "..."} for: hi'
```

Rules:
1. Never let users supply the format string. Format strings can traverse attributes and indexes.
2. Values passed into `.format()` are not re-interpreted, so user values are safe as arguments. The danger is user text becoming the template.
3. Templates containing JSON examples need `{{ }}` escaping, or use `string.Template` or Jinja2, where braces aren't special.

## Likely follow-ups

- What does Jinja2's `SandboxedEnvironment` protect against?

---

[← Q0165](../../batch_02_prompting_context_structured_output/0165_check_required_sections_in_generated_reports/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0167 →](../../batch_02_prompting_context_structured_output/0167_log_prompt_metadata_for_traceability/README.md)

# Q0165 · Check required sections in generated reports

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Output validation | Easy |

## Question

A generated incident report must contain the headings Summary, Impact, Root Cause and Actions, in that order. Write a validator that reports missing and out-of-order sections.

## Answer

```python
import re


def check_sections(markdown: str, required: list[str]) -> dict:
    found = [h.strip() for h in re.findall(r"^#{1,3}\s+(.+?)\s*$", markdown, re.M)]
    positions = {name: found.index(name) for name in required if name in found}
    missing = [name for name in required if name not in positions]
    present = [name for name in required if name in positions]
    in_order = [p for p in sorted(present, key=positions.get)] == present
    return {"missing": missing, "in_order": in_order}


report = "## Summary\nDB failover.\n## Root Cause\nExpired cert.\n## Impact\n20 min outage.\n"
res = check_sections(report, ["Summary", "Impact", "Root Cause", "Actions"])
assert res == {"missing": ["Actions"], "in_order": False}
good = "# Summary\n..\n# Impact\n..\n# Root Cause\n..\n# Actions\n.."
assert check_sections(good, ["Summary", "Impact", "Root Cause", "Actions"]) == {"missing": [], "in_order": True}
```

For machine-consumed reports, generating a JSON object with one field per section (then rendering markdown in code) is more robust than validating free-form headings.

## Likely follow-ups

- Why is "generate JSON, render markdown in code" more reliable?

---

[← Q0164](../../batch_02_prompting_context_structured_output/0164_generate_critique_and_revise_loop/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0166 →](../../batch_02_prompting_context_structured_output/0166_avoid_str_format_injection_in_templates/README.md)

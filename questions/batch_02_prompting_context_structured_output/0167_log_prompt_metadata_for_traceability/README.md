# Q0167 · Log prompt metadata for traceability

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Observability | Medium |

## Question

Build a log record for each LLM call that makes the response traceable (prompt name and version, a hash of the rendered prompt, model and parameters) without storing raw prompt text or raw user identifiers by default.

## Answer

```python
import hashlib
import hmac


def llm_call_record(prompt_name: str, prompt_version: str, rendered: str, model: str, params: dict,
                    user_id: str, pseudonym_key: bytes, trace_id: str) -> dict:
    return {
        "trace_id": trace_id,
        "prompt": f"{prompt_name}@{prompt_version}",
        "prompt_sha256": hashlib.sha256(rendered.encode()).hexdigest()[:16],
        "prompt_chars": len(rendered),
        "model": model,
        "params": {k: params[k] for k in sorted(params) if k in {"temperature", "top_p", "max_tokens", "seed"}},
        "user": hmac.new(pseudonym_key, user_id.encode(), hashlib.sha256).hexdigest()[:16],
    }


rec = llm_call_record("policy_qa", "1.3.0", "System...\nQuestion: salary bands?", "gpt-x-2026-05-01",
                      {"temperature": 0.2, "max_tokens": 800, "api_key": "sk-leak"}, "jdoe@corp",
                      b"rotate-me", "t-123")
assert rec["prompt"] == "policy_qa@1.3.0" and "api_key" not in rec["params"]
assert "jdoe" not in str(rec) and len(rec["user"]) == 16
assert rec == llm_call_record("policy_qa", "1.3.0", "System...\nQuestion: salary bands?", "gpt-x-2026-05-01",
                              {"temperature": 0.2, "max_tokens": 800}, "jdoe@corp", b"rotate-me", "t-123")
```

An HMAC with a secret key (rather than a plain hash) stops anyone from brute-forcing user ids back from the logs. Full prompts and responses may still be needed for audit or evaluation: store them in a separate, access-controlled store with retention rules, linked by `trace_id`. The parameter allowlist also stops secrets from leaking into logs.

## Likely follow-ups

- Which teams should be able to see full prompt and response content, and under what controls?

---

[← Q0166](../../batch_02_prompting_context_structured_output/0166_avoid_str_format_injection_in_templates/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0168 →](../../batch_02_prompting_context_structured_output/0168_compare_two_prompts_on_a_dev_set/README.md)

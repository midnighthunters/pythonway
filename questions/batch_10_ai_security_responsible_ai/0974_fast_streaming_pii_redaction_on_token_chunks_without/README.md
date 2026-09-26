# Q0974 · Fast streaming PII redaction on token chunks without buffering entire responses

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain the windowing buffer technique for streaming PII redaction, and write Python code implementing sliding-window regex redaction over streaming token chunks.

## Answer

When streaming tokens via Server-Sent Events (SSE), waiting for the entire 2,000-token response to complete before redacting PII destroys the streaming user experience (TTFT drops to 15 seconds).

However, token chunks arrive piecemeal: `"123-"`, `"45-"`, `"6789"`. Evaluating regex on single isolated tokens fails to match the SSN!

**Sliding-Window Buffer**:
Maintains an internal buffer of $N$ characters (e.g. 30 chars). Chunks are appended to the buffer, regex is evaluated on the buffer, and safe leading text is yielded while the trailing tail is held for cross-boundary matches.

```python
from typing import Generator, List
import re


class StreamingPIIRedactor:
    def __init__(self, window_size: int = 15):
        self.buffer = ""
        self.window_size = window_size
        self.ssn_pattern = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

    def process_chunk(self, chunk: str) -> str:
        self.buffer += chunk
        # Check for matches in current buffer
        self.buffer = self.ssn_pattern.sub("[REDACTED_SSN]", self.buffer)

        # If buffer exceeds window size, yield safe leading characters
        if len(self.buffer) > self.window_size:
            emit_len = len(self.buffer) - self.window_size
            to_emit = self.buffer[:emit_len]
            self.buffer = self.buffer[emit_len:]
            return to_emit
        return ""

    def flush(self) -> str:
        # Final cleanup pass on remaining buffer
        final_str = self.ssn_pattern.sub("[REDACTED_SSN]", self.buffer)
        self.buffer = ""
        return final_str


redactor = StreamingPIIRedactor(window_size=15)
chunks = ["Client SSN ", "is 123", "-45", "-6789", " recorded."]

streamed_output = ""
for c in chunks:
    streamed_output += redactor.process_chunk(c)
streamed_output += redactor.flush()

assert "123-45-6789" not in streamed_output
assert "[REDACTED_SSN]" in streamed_output
assert "Client SSN is [REDACTED_SSN] recorded." == streamed_output
```

## Likely follow-ups

- What is the latency impact of holding a 15-character trailing window during SSE streaming?
- How do you handle entities that span across arbitrary token boundaries in multi-byte Unicode?

---

[← Q0973](../../batch_10_ai_security_responsible_ai/0973_evaluating_pii_redaction_precision_recall_and_false/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0975 →](../../batch_10_ai_security_responsible_ai/0975_end_to_end_pii_anonymization_and_de_anonymization_gateway/README.md)

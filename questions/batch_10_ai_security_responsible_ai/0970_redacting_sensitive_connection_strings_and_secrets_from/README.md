# Q0970 · Redacting sensitive connection strings and secrets from agent traceback outputs

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Easy |

## Question

Write Python code implementing an exception interceptor that redacts database connection strings, passwords, and API tokens from error tracebacks before returning responses to the user.

## Answer

When a Python database tool crashes (e.g. `sqlalchemy.exc.OperationalError`), the default traceback prints the raw connection string:
`postgresql://dbadmin:P@ssw0rd123@db-prod.internal:5432/trades`
Exposing this traceback to an external user constitutes a high-severity security incident.

```python
import re
from typing import Tuple


def sanitize_traceback_string(error_msg: str) -> str:
    # Pattern matching database URIs with embedded credentials
    db_uri_pattern = re.compile(
        r"(postgresql|mysql|mongodb|redis|mssql)://(?P<user>[^:]+):(?P<pass>[^@]+)@(?P<host>[^:/]+)",
        re.IGNORECASE,
    )
    # Strip API tokens and bearer headers
    token_pattern = re.compile(r"(bearer\s+|token\s+|key=)[a-zA-Z0-9_\-\.]{15,}", re.IGNORECASE)

    clean = db_uri_pattern.sub(r"\1://[REDACTED_USER]:[REDACTED_PW]@\4", error_msg)
    clean = token_pattern.sub(r"\1[REDACTED_SECRET]", clean)
    return clean


crash_trace = (
    "OperationalError: connection to postgresql://trader_svc:SuperSecretPass99@db-cluster.internal:5432/trades failed. "
    "Auth token: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6..."
)

sanitized = sanitize_traceback_string(crash_trace)
assert "SuperSecretPass99" not in sanitized
assert "eyJhbGciOi" not in sanitized
assert "postgresql://[REDACTED_USER]:[REDACTED_PW]@db-cluster.internal" in sanitized
assert "Bearer [REDACTED_SECRET]" in sanitized
```

## Likely follow-ups

- Why should raw stack traces never be displayed in production API responses (HTTP 500)?
- How do structured error envelopes (RFC 7807 Problem Details) standardize error responses safely?

---

[← Q0969](../../batch_10_ai_security_responsible_ai/0969_synthetic_data_generation_for_testing_rag_without_exposing/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0971 →](../../batch_10_ai_security_responsible_ai/0971_optical_character_recognition_pii_scrubbing_from_uploaded/README.md)

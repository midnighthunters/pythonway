# Q0975 · End-to-end PII anonymization and de-anonymization gateway

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Write Python code implementing an end-to-end PII proxy gateway: ingests user prompt, detects and tokenizes PII, calls mock LLM, and de-tokenizes response before client return.

## Answer

An enterprise GenAI privacy gateway sits between the corporate client and the external foundation model. It guarantees that the external model provider never sees real customer names, account numbers, or tax identifiers.

```python
import re
from typing import Dict, Tuple


class EnterprisePrivacyGateway:
    def __init__(self):
        self.entity_pattern = re.compile(r"\b(John Doe|Alice Smith|ACC-\d{5})\b")

    def forward_pass(self, prompt: str) -> Tuple[str, Dict[str, str]]:
        lookup = {}
        counter = 0

        def replace_fn(match):
            nonlocal counter
            val = match.group(0)
            if val not in lookup:
                counter += 1
                token = f"CUST_TOKEN_{counter}"
                lookup[token] = val
            else:
                # Find existing token
                token = [k for k, v in lookup.items() if v == val][0]
            return token

        sanitized_prompt = self.entity_pattern.sub(replace_fn, prompt)
        return sanitized_prompt, lookup

    def reverse_pass(self, model_response: str, lookup: Dict[str, str]) -> str:
        restored = model_response
        for token, original_val in lookup.items():
            restored = restored.replace(token, original_val)
        return restored


gateway = EnterprisePrivacyGateway()
client_prompt = "Transfer funds from John Doe (ACC-10029) to Alice Smith (ACC-88123)."

# 1. Forward Pass (Anonymization)
clean_prompt, token_table = gateway.forward_pass(client_prompt)
assert "John Doe" not in clean_prompt
assert "ACC-10029" not in clean_prompt
assert "CUST_TOKEN_1" in clean_prompt

# 2. Simulated External LLM Completion
llm_output = f"Processed wire request: Debited CUST_TOKEN_2, credited CUST_TOKEN_4 for CUST_TOKEN_1."

# 3. Reverse Pass (De-anonymization inside bank firewall)
final_response = gateway.reverse_pass(llm_output, token_table)
assert "John Doe" in final_response
assert "ACC-10029" in final_response
assert "CUST_TOKEN_" not in final_response
```

## Likely follow-ups

- How does the privacy gateway log audit entries without writing raw PII to plaintext log files?
- How is the temporary lookup table isolated between concurrent user requests?

---

[← Q0974](../../batch_10_ai_security_responsible_ai/0974_fast_streaming_pii_redaction_on_token_chunks_without/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0976 →](../../batch_10_ai_security_responsible_ai/0976_federal_reserve_sr_11_7_and_occ_2011_12_model_risk/README.md)

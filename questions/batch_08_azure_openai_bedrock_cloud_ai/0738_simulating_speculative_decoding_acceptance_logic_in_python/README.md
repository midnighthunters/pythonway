# Q0738 · Simulating speculative decoding acceptance logic in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Hard |

## Question

Write Python code that simulates speculative decoding acceptance, comparing draft tokens against target tokens and verifying accepted sequences.

## Answer

```python
from typing import List, Tuple


def evaluate_speculative_tokens(draft_tokens: List[str], target_validations: List[bool]) -> Tuple[List[str], int]:
    accepted = []
    for token, is_valid in zip(draft_tokens, target_validations):
        if is_valid:
            accepted.append(token)
        else:
            break  # Reject first invalid token and abort subsequent speculative tokens
    return accepted, len(accepted)


# Target model verifies first 3 draft tokens, rejects 4th
draft = ["The", "quarterly", "earnings", "skyrocketed", "unexpectedly"]
validations = [True, True, True, False, True]

accepted_tokens, count = evaluate_speculative_tokens(draft, validations)
assert count == 3
assert accepted_tokens == ["The", "quarterly", "earnings"]
```

## Likely follow-ups

- How does temperature sampling modify the acceptance criterion in speculative decoding?
- Why does speculative decoding maintain identical output distributions to standard target model generation?

---

[← Q0737](../../batch_08_azure_openai_bedrock_cloud_ai/0737_speculative_decoding_draft_model_plus_target_model/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0739 →](../../batch_08_azure_openai_bedrock_cloud_ai/0739_prefix_caching_and_prompt_caching_across_multi_turn_sessions/README.md)

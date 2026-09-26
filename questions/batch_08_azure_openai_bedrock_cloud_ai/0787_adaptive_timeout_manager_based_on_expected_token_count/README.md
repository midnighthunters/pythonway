# Q0787 · Adaptive timeout manager based on expected token count

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Write Python code that computes an adaptive request timeout based on input prompt length and requested `max_tokens`.

## Answer

```python
class AdaptiveTimeoutCalculator:
    def __init__(self, base_overhead_sec: float = 2.0, sec_per_100_tokens: float = 0.5):
        self.base_overhead = base_overhead_sec
        self.sec_per_100_tokens = sec_per_100_tokens

    def calculate_timeout(self, prompt_tokens: int, max_completion_tokens: int) -> float:
        # Prefill time estimate
        prefill_time = (prompt_tokens / 100.0) * (self.sec_per_100_tokens * 0.2)
        # Generation time estimate
        generation_time = (max_completion_tokens / 100.0) * self.sec_per_100_tokens
        total_estimate = self.base_overhead + prefill_time + generation_time
        # Add 50% safety buffer
        return round(total_estimate * 1.5, 2)


calc = AdaptiveTimeoutCalculator(base_overhead_sec=2.0, sec_per_100_tokens=0.5)

# Short request: 100 prompt, 50 completion
t_short = calc.calculate_timeout(prompt_tokens=100, max_completion_tokens=50)
assert 3.0 <= t_short <= 6.0

# Long generation: 10,000 prompt, 4,000 completion
t_long = calc.calculate_timeout(prompt_tokens=10000, max_completion_tokens=4000)
assert t_long > 30.0
```

## Likely follow-ups

- Why is adaptive timeout essential for batch summarization pipelines?
- How should the timeout adapt if the provider is experiencing high global utilization?

---

[← Q0786](../../batch_08_azure_openai_bedrock_cloud_ai/0786_client_side_timeout_strategies_for_streaming_vs_non/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0788 →](../../batch_08_azure_openai_bedrock_cloud_ai/0788_token_estimation_using_model_tokenizers_before_cloud_api/README.md)

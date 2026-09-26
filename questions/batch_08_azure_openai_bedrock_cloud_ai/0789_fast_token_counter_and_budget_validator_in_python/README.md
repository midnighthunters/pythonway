# Q0789 · Fast token counter and budget validator in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Write Python code for a request admission controller that validates whether an incoming prompt fits within both the model context window and the tenant's daily token budget.

## Answer

```python
from typing import Dict, Tuple


class TokenAdmissionController:
    def __init__(self, model_max_context: int, tenant_daily_budget: int):
        self.model_max_context = model_max_context
        self.tenant_daily_budget = tenant_daily_budget
        self.tenant_spent: Dict[str, int] = {}

    def admit_request(self, tenant_id: str, prompt_tokens: int, max_tokens: int) -> Tuple[bool, str]:
        total_requested = prompt_tokens + max_tokens

        # Check model context window
        if total_requested > self.model_max_context:
            return False, f"Context window exceeded: {total_requested} > {self.model_max_context}"

        current_spent = self.tenant_spent.get(tenant_id, 0)
        if current_spent + total_requested > self.tenant_daily_budget:
            return False, f"Daily budget exceeded for {tenant_id}: {current_spent + total_requested} > {self.tenant_daily_budget}"

        # Reserve tokens
        self.tenant_spent[tenant_id] = current_spent + total_requested
        return True, "Admitted"


controller = TokenAdmissionController(model_max_context=8192, tenant_daily_budget=50000)

# Valid admission
ok1, _ = controller.admit_request("desk-fx", prompt_tokens=1000, max_tokens=500)
assert ok1 is True

# Context window exceeded
ok2, msg2 = controller.admit_request("desk-fx", prompt_tokens=7000, max_tokens=2000)
assert ok2 is False
assert "Context window exceeded" in msg2

# Budget exceeded
controller.tenant_spent["desk-fx"] = 45000
ok3, msg3 = controller.admit_request("desk-fx", prompt_tokens=4000, max_tokens=2000)
assert ok3 is False
assert "Daily budget exceeded" in msg3
```

## Likely follow-ups

- How should unspent reserved tokens be refunded if generation stops early at token 100?
- How are multi-modal image token budgets calculated before sending to vision models?

---

[← Q0788](../../batch_08_azure_openai_bedrock_cloud_ai/0788_token_estimation_using_model_tokenizers_before_cloud_api/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0790 →](../../batch_08_azure_openai_bedrock_cloud_ai/0790_key_rotation_and_credential_reloading_without_service/README.md)

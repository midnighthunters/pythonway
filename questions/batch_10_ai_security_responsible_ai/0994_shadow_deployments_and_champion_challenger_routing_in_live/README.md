# Q0994 · Shadow deployments and champion-challenger routing in live banking traffic

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Write Python code implementing an asynchronous shadow deployment router that sends 100% of live traffic to the production champion model while mirroring traffic to a shadow challenger model for telemetry.

## Answer

In banking, directly replacing a production model with a new model risks unexpected regressions. In a **Shadow Deployment (Dark Launch)**:
1. Live user traffic is routed to the Champion model; the user receives the Champion's response immediately.
2. The exact same prompt is asynchronously mirrored to the Challenger model in the background.
3. Both responses, latencies, and token counts are logged side-by-side in an audit database for evaluation.

```python
import asyncio
from typing import Dict, Any


class ShadowDeploymentRouter:
    def __init__(self):
        self.shadow_logs: list[dict] = []

    async def _call_champion(self, prompt: str) -> str:
        await asyncio.sleep(0.01)
        return f"Champion output for: {prompt}"

    async def _call_shadow_challenger(self, prompt: str, champ_output: str):
        await asyncio.sleep(0.02)
        chall_output = f"Challenger output for: {prompt}"
        # Log comparison in telemetry database
        self.shadow_logs.append({
            "prompt": prompt,
            "champion_response": champ_output,
            "challenger_response": chall_output,
        })

    async def handle_request(self, prompt: str) -> str:
        # Step 1: Execute champion synchronously for user
        champ_res = await self._call_champion(prompt)

        # Step 2: Fire-and-forget shadow call in background
        asyncio.create_task(self._call_shadow_challenger(prompt, champ_res))

        # Return champion result immediately without waiting for shadow
        return champ_res


async def main():
    router = ShadowDeploymentRouter()
    user_reply = await router.handle_request("Explain SOFR swap spreads")

    assert "Champion output" in user_reply
    assert len(router.shadow_logs) == 0  # Shadow still executing in background

    await asyncio.sleep(0.04)  # Allow background shadow task to finish
    assert len(router.shadow_logs) == 1
    assert "Challenger output" in router.shadow_logs[0]["challenger_response"]


asyncio.run(main())
```

## Likely follow-ups

- Why must shadow requests be strictly decoupled from database mutations (read-only execution)?
- What compute and token cost overhead is incurred by running a 100% shadow deployment?

---

[← Q0993](../../batch_10_ai_security_responsible_ai/0993_semantic_drift_detection_and_output_distribution_shifts_in/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0995 →](../../batch_10_ai_security_responsible_ai/0995_incident_response_playbook_for_genai_security_breach/README.md)

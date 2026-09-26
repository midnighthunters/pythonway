# Q0948 · Preventing recursive agent loop runaway and infinite loop detection

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Write Python code implementing an infinite loop detector for multi-agent systems, detecting repeated identical tool calls with identical parameters.

## Answer

When an agent encounters an unexpected tool error (e.g. "Ticker symbol not found"), a poorly prompted agent may repeatedly invoke the exact same tool with the exact same bad parameter, burning API tokens endlessly.

Loop detection tracks recent `(tool_name, params_hash)` history and aborts upon detecting cyclical repetition.

```python
import hashlib
import json
from typing import List


class AgentLoopDetector:
    def __init__(self, max_consecutive_duplicates: int = 2):
        self.history: List[str] = []
        self.max_duplicates = max_consecutive_duplicates

    def record_call(self, tool_name: str, params: dict) -> bool:
        # Compute signature hash of tool and parameters
        sig = f"{tool_name}:{json.dumps(params, sort_keys=True)}"
        h = hashlib.sha256(sig.encode()).hexdigest()
        self.history.append(h)

        # Check if the last N calls are identical
        if len(self.history) >= self.max_duplicates:
            last_n = self.history[-self.max_duplicates :]
            if len(set(last_n)) == 1:
                return True  # Infinite loop detected!
        return False


detector = AgentLoopDetector(max_consecutive_duplicates=3)

# Distinct calls
assert detector.record_call("get_quote", {"ticker": "AAPL"}) is False
assert detector.record_call("get_quote", {"ticker": "MSFT"}) is False

# Identical repeated calls
assert detector.record_call("bad_tool", {"arg": 1}) is False
assert detector.record_call("bad_tool", {"arg": 1}) is False
# 3rd identical call triggers loop detection
assert detector.record_call("bad_tool", {"arg": 1}) is True
```

## Likely follow-ups

- What subtle loop patterns (e.g. A -> B -> A -> B cycles) require cycle-detection algorithms (like Floyd's cycle-finding)?
- How does LangGraph handle graph cycle recursion limits?

---

[← Q0947](../../batch_10_ai_security_responsible_ai/0947_dual_custody_and_4_eyes_principle_enforcement_for_financial/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0949 →](../../batch_10_ai_security_responsible_ai/0949_agent_tool_call_parameter_schema_validation_with_pydantic_v2/README.md)

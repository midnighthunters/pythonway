# Q0995 · Incident response playbook for GenAI security breach

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Outline an Incident Response Playbook for a Generative AI security incident (prompt leakage or unauthorized tool execution), and write Python code implementing an automated quarantine kill-switch.

## Answer

GenAI Incident Response Playbook:
1. **Identification**: Alert fired from Canary token detector, excessive tool rate governor, or SIEM.
2. **Containment (Kill Switch)**: Immediately revoke the compromised agent's tool permissions, terminate active sessions, and route traffic to a static maintenance response.
3. **Eradication**: Identify the root-cause prompt injection vector, update system prompts/guardrails, and patch regex/classifiers.
4. **Recovery**: Deploy updated guardrails to staging, run red-team eval battery, and resume production traffic.
5. **Post-Mortem & Reporting**: Formal disclosure to Model Risk Office, CISO, and regulatory bodies (within 72h under NYDFS).

```python
class AgentKillSwitchManager:
    def __init__(self):
        self.is_quarantined = False
        self.active_sessions_killed = 0

    def trigger_emergency_quarantine(self, incident_reason: str) -> dict:
        self.is_quarantined = True
        self.active_sessions_killed += 42  # Kill all active agent sessions
        return {
            "status": "QUARANTINED",
            "reason": incident_reason,
            "traffic_diverted_to_fallback": True,
        }

    def process_incoming_request(self, user_prompt: str) -> str:
        if self.is_quarantined:
            return "SERVICE UNAVAILABLE: GenAI assistant is temporarily offline for maintenance."
        return f"Normal answer to: {user_prompt}"


mgr = AgentKillSwitchManager()
assert "Normal answer" in mgr.process_incoming_request("Market status")

# Security incident detected: trigger kill switch
report = mgr.trigger_emergency_quarantine("Canary token leak detected in session 882")
assert report["status"] == "QUARANTINED"
assert mgr.is_quarantined is True

# Subsequent requests are safely blocked
res = mgr.process_incoming_request("Market status")
assert "temporarily offline" in res
```

## Likely follow-ups

- Who has the executive authority to trip the emergency kill switch in an investment bank?
- How do Feature Flags (e.g. LaunchDarkly) enable sub-second emergency disablement?

---

[← Q0994](../../batch_10_ai_security_responsible_ai/0994_shadow_deployments_and_champion_challenger_routing_in_live/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0996 →](../../batch_10_ai_security_responsible_ai/0996_explainability_and_explainable_ai_xai_requirements_in/README.md)

# Q0939 · Agent impersonation and synthetic identity spoofing

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Explain agent impersonation attacks in multi-agent systems, and write Python code implementing HMAC digital signatures to verify agent-to-agent message authenticity.

## Answer

In an open agent mesh (e.g., A2A protocol), a rogue agent can craft messages claiming to originate from the "Chief Risk Officer Agent" and order other agents to liquidate assets.

To prevent identity spoofing, all inter-agent messages must carry an HMAC digital signature or asymmetric ECDSA signature verified by the recipient.

```python
import hmac
import hashlib
import json
from typing import Dict, Any, Tuple


class AgentMessageSigner:
    def __init__(self, agent_id: str, shared_secret: bytes):
        self.agent_id = agent_id
        self.secret = shared_secret

    def sign_message(self, payload: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        serialized = json.dumps(payload, sort_keys=True)
        signature = hmac.new(self.secret, serialized.encode(), hashlib.sha256).hexdigest()
        return payload, signature

    def verify_message(self, payload: Dict[str, Any], signature: str) -> bool:
        serialized = json.dumps(payload, sort_keys=True)
        expected = hmac.new(self.secret, serialized.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)


signer = AgentMessageSigner("RiskOfficerAgent", b"secret_risk_bus_key")
data = {"command": "HALT_TRADING", "desk": "FX_SPOT"}

msg, sig = signer.sign_message(data)
assert signer.verify_message(msg, sig) is True

# Attacker tampers with desk parameter
tampered_msg = {"command": "HALT_TRADING", "desk": "EQUITIES"}
assert signer.verify_message(tampered_msg, sig) is False
```

## Likely follow-ups

- What are the operational challenges of managing symmetric HMAC keys across hundreds of microservices?
- How do PKI certificates and mutual TLS (mTLS) provide asymmetric identity verification?

---

[← Q0938](../../batch_10_ai_security_responsible_ai/0938_step_up_authentication_and_totp_verification_in_agent/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0940 →](../../batch_10_ai_security_responsible_ai/0940_server_side_request_forgery_prevention_in_agent_web/README.md)

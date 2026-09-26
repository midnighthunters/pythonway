# Q0869 · OAuth2 JWT bearer token validation with role-based access control

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code implementing JWT Bearer token authentication and Role-Based Access Control (RBAC) in FastAPI using simulated secret verification.

## Answer

Enterprise users accessing the LLM Suite possess fine-grained roles (e.g. `ANALYST`, `COMPLIANCE_OFFICER`, `TRADER`). Endpoints must verify token validity and ensure the caller's role permits the requested action.

```python
import base64
import json
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient

app = FastAPI()
security = HTTPBearer()


def mock_decode_jwt(token: str) -> dict:
    # Simulated JWT payload decoding
    try:
        payload_str = base64.b64decode(token.encode()).decode()
        return json.loads(payload_str)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def require_role(required_role: str):
    def role_checker(creds: HTTPAuthorizationCredentials = Depends(security)):
        payload = mock_decode_jwt(creds.credentials)
        roles = payload.get("roles", [])
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required",
            )
        return payload
    return role_checker


@app.get("/compliance/audit-log")
def read_audit(user: dict = Depends(require_role("COMPLIANCE_OFFICER"))):
    return {"audit_data": "Audit entries", "caller": user.get("sub")}


client = TestClient(app)

# Valid compliance user
user_payload = base64.b64encode(json.dumps({"sub": "user_42", "roles": ["COMPLIANCE_OFFICER"]}).encode()).decode()
res = client.get("/compliance/audit-log", headers={"Authorization": f"Bearer {user_payload}"})
assert res.status_code == 200
assert res.json()["caller"] == "user_42"

# Trader user attempting access
trader_payload = base64.b64encode(json.dumps({"sub": "trader_10", "roles": ["TRADER"]}).encode()).decode()
res_denied = client.get("/compliance/audit-log", headers={"Authorization": f"Bearer {trader_payload}"})
assert res_denied.status_code == 403
```

## Likely follow-ups

- How does JSON Web Key Set (JWKS) caching prevent calling Entra ID / Okta on every request?
- What is the difference between Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC)?

---

[← Q0868](../../batch_09_genai_services_fastapi/0868_mutual_tls_client_certificate_authentication_in_fastapi/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0870 →](../../batch_09_genai_services_fastapi/0870_cors_csrf_and_security_headers_middleware_for_genai/README.md)

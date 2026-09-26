# Q0803 · FastAPI dependency injection for tenant identification and auth

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code demonstrating FastAPI dependency injection (`Depends`) to extract and validate an enterprise Bearer token and inject a `TenantContext` into route handlers.

## Answer

In multi-tenant banking platforms (like JPMC LLM Suite), every API request must be authenticated, authorized, and mapped to a specific department or tenant ID for billing and auditing.

```python
from typing import Annotated, Dict
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel


class TenantContext(BaseModel):
    tenant_id: str
    department: str
    tier: str


MOCK_TOKEN_DB = {
    "token-equities-123": TenantContext(tenant_id="ten-eq-01", department="Equities", tier="premium"),
    "token-fixed-456": TenantContext(tenant_id="ten-fi-02", department="Fixed Income", tier="standard"),
}


def get_current_tenant(authorization: Annotated[str, Header()] = None) -> TenantContext:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
        )
    token = authorization[7:]
    context = MOCK_TOKEN_DB.get(token)
    if not context:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired tenant token",
        )
    return context


app = FastAPI()


@app.get("/quota")
def check_quota(tenant: TenantContext = Depends(get_current_tenant)):
    return {"tenant_id": tenant.tenant_id, "department": tenant.department, "limit_tpm": 100000}


client = TestClient(app)

# Authorized call
res = client.get("/quota", headers={"Authorization": "Bearer token-equities-123"})
assert res.status_code == 200
assert res.json()["department"] == "Equities"

# Unauthorized call
bad_res = client.get("/quota", headers={"Authorization": "Bearer invalid-token"})
assert bad_res.status_code == 403
```

## Likely follow-ups

- How does dependency injection simplify unit testing via `app.dependency_overrides`?
- How can dependencies be scoped at the APIRouter level rather than repeated on individual routes?

---

[← Q0802](../../batch_09_genai_services_fastapi/0802_pydantic_v2_request_and_response_validation_for_chat/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0804 →](../../batch_09_genai_services_fastapi/0804_preventing_event_loop_blocking_in_async_fastapi_routes/README.md)

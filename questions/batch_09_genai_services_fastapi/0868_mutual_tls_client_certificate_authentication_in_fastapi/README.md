# Q0868 · Mutual TLS client certificate authentication in FastAPI

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Explain how Mutual TLS (mTLS) secures inter-service communications for GenAI microservices, and write Python code simulating client certificate SAN/CN verification in middleware.

## Answer

In Zero-Trust banking environments, internal microservices communicate over mTLS. The TLS handshake verifies both the server's certificate and the client's certificate. The reverse proxy (Nginx, Envoy, or AWS ALB) terminates TLS and forwards the client's certificate subject (Common Name / SAN) in an HTTP header (e.g. `X-Client-Cert-Subject`).

```python
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.testclient import TestClient

app = FastAPI()

AUTHORIZED_SERVICES = {"trade-break-service.internal", "risk-orchestrator.internal"}


@app.get("/internal/admin/purge-cache")
def purge_cache(x_client_cert_cn: Optional[str] = Header(None)):
    if not x_client_cert_cn or x_client_cert_cn not in AUTHORIZED_SERVICES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized service certificate",
        )
    return {"status": "cache purged", "authorized_as": x_client_cert_cn}


client = TestClient(app)

# Authorized client service
r_ok = client.get("/internal/admin/purge-cache", headers={"X-Client-Cert-CN": "trade-break-service.internal"})
assert r_ok.status_code == 200
assert r_ok.json()["status"] == "cache purged"

# Unauthorized or untrusted service
r_bad = client.get("/internal/admin/purge-cache", headers={"X-Client-Cert-CN": "untrusted-script.internal"})
assert r_bad.status_code == 403
```

## Likely follow-ups

- Why must internal headers injected by reverse proxies be stripped from inbound public perimeter requests?
- How does Istio service mesh automate mTLS sidecar proxying without modifying application Python code?

---

[← Q0867](../../batch_09_genai_services_fastapi/0867_sub_applications_and_api_versioning_with_apirouter/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0869 →](../../batch_09_genai_services_fastapi/0869_oauth2_jwt_bearer_token_validation_with_role_based_access/README.md)

# Q0870 · CORS, CSRF, and security headers middleware for GenAI frontends

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Easy |

## Question

Write Python code configuring CORS and security headers (CSP, HSTS, X-Content-Type-Options) in a FastAPI application hosting interactive GenAI web interfaces.

## Answer

GenAI frontends interacting with backend APIs require strict Cross-Origin Resource Sharing (CORS) rules to prevent malicious websites from executing cross-site requests using stolen session cookies.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://llmsuite.jpmc.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# 2. Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response


app.add_middleware(SecurityHeadersMiddleware)


@app.get("/ping")
def ping():
    return {"ping": "pong"}


client = TestClient(app)
res = client.get("/ping")

assert res.status_code == 200
assert res.headers["x-frame-options"] == "DENY"
assert res.headers["x-content-type-options"] == "nosniff"
assert "max-age=31536000" in res.headers["strict-transport-security"]
```

## Likely follow-ups

- Why should `allow_origins=["*"]` never be combined with `allow_credentials=True`?
- How does Content Security Policy (CSP) prevent stored XSS attacks in LLM markdown renderers?

---

[← Q0869](../../batch_09_genai_services_fastapi/0869_oauth2_jwt_bearer_token_validation_with_role_based_access/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0871 →](../../batch_09_genai_services_fastapi/0871_arq_async_redis_job_queue_implementation_for_long_running/README.md)

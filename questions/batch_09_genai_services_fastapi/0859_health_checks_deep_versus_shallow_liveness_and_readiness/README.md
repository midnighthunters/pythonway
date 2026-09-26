# Q0859 · Health checks: Deep versus shallow liveness and readiness probes

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Easy |

## Question

Write Python code implementing `/livez` (liveness) and `/readyz` (readiness) probe endpoints in FastAPI, distinguishing process vitality from dependency availability.

## Answer

In Kubernetes:
- **Liveness Probe (`/livez`)**: Checks if the container process is alive and responsive. If it fails, Kubernetes restarts the pod. Should be **shallow** (does not check external databases).
- **Readiness Probe (`/readyz`)**: Checks if the pod can accept user traffic (verifies Redis connection, model weights loaded, vector index accessible). If it fails, Kubernetes temporarily cuts traffic from the Service endpoint.

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

app = FastAPI()

# Simulated service state
app.state.is_healthy = True
app.state.redis_connected = True
app.state.model_weights_loaded = True


@app.get("/livez")
def liveness():
    '''Shallow check: returns 200 if event loop is running.'''
    if not app.state.is_healthy:
        raise HTTPException(status_code=503, detail="Unhealthy")
    return {"status": "alive"}


@app.get("/readyz")
def readiness():
    '''Deep check: returns 200 only if all critical dependencies are ready.'''
    if not (app.state.redis_connected and app.state.model_weights_loaded):
        raise HTTPException(status_code=503, detail="Dependencies not ready")
    return {"status": "ready"}


client = TestClient(app)

# Both pass initially
assert client.get("/livez").status_code == 200
assert client.get("/readyz").status_code == 200

# Redis connection drops
app.state.redis_connected = False
# Process is still alive (no pod restart needed)
assert client.get("/livez").status_code == 200
# But cannot serve traffic (Kubernetes removes pod from load balancer pool)
assert client.get("/readyz").status_code == 503
```

## Likely follow-ups

- Why must deep readiness probes have a reasonable timeout (e.g. 2-5 seconds)?
- What catastrophic cascade occurs if an external database outage causes all `/livez` probes to fail?

---

[← Q0858](../../batch_09_genai_services_fastapi/0858_prometheus_metrics_endpoint_for_request_counts_latencies/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0860 →](../../batch_09_genai_services_fastapi/0860_request_body_streaming_and_large_file_upload_for_document/README.md)

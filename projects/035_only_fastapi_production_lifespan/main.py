"""
===============================================================================
PROJECT 035: PRODUCTION FASTAPI: LIFESPAN HANDLERS, LOGGING & HEALTH PROBES
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do enterprise systems guarantee zero-downtime deployments, graceful
connection draining, pre-warmed AI models, and machine-readable structured
telemetry under Kubernetes/production orchestrators?

PRODUCTION PATTERNS IMPLEMENTED:
1. Modern Lifespan Context Manager (@asynccontextmanager):
   - Deterministic resource initialization before accepting traffic.
   - Clean connection pool draining and shutdown telemetry.
2. Structured JSON Logging:
   - Machine-parsable JSON logs with trace_id correlation across handlers.
3. Dual Kubernetes Health Probes:
   - Liveness Probe (/health/live): Verifies process vitality.
   - Readiness Probe (/health/ready): Evaluates database, cache, and LLM readiness.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import uuid
import json
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STRUCTURED JSON LOGGING ENGINE
# =============================================================================
class JSONLogFormatter(logging.Formatter):
    """Formats log records as uniform, single-line JSON objects for log aggregators."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": "cafe-production-gateway",
        }
        if hasattr(record, "trace_id"):
            log_payload["trace_id"] = record.trace_id
        if hasattr(record, "extra_data"):
            log_payload["extra"] = record.extra_data
        return json.dumps(log_payload)


logger = logging.getLogger("production.gateway")
logger.setLevel(logging.INFO)
# Clear existing handlers to prevent duplicates
logger.handlers.clear()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONLogFormatter())
logger.addHandler(handler)


# =============================================================================
# 2. LIFESPAN CONTEXT MANAGER
# =============================================================================
APP_START_TIME = time.time()


class SimulatedDatabasePool:
    """Simulates an enterprise async connection pool."""

    def __init__(self):
        self.connected = False
        self.active_connections = 0

    async def connect(self):
        self.connected = True
        self.active_connections = 5

    async def ping(self) -> bool:
        return self.connected

    async def close(self):
        self.connected = False
        self.active_connections = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager replacing deprecated @app.on_event('startup'/'shutdown').
    Code before 'yield' runs on server startup.
    Code after 'yield' runs on server shutdown.
    """
    logger.info("Lifespan startup sequence initiated...")

    # 1. Initialize State Container
    app.state.db_pool = SimulatedDatabasePool()
    await app.state.db_pool.connect()

    # 2. Warm up LLM client
    logger.info(f"Pre-warming LLM client with active model: {ACTIVE_MODEL}")
    app.state.llm = get_llm(temperature=0.3)

    # 3. Mark ready
    app.state.is_ready = True
    app.state.is_live = True
    app.state.startup_timestamp = time.time()
    logger.info("Application lifespan successfully initialized. Traffic accepted.")

    # Yield control to the ASGI application
    yield

    # Shutdown sequence
    logger.info("Lifespan shutdown sequence triggered. Draining connections...")
    app.state.is_ready = False
    await app.state.db_pool.close()
    logger.info("All connection pools closed. Clean shutdown complete.")


# =============================================================================
# 3. FASTAPI APPLICATION & TRACE MIDDLEWARE
# =============================================================================
app = FastAPI(
    title="Cozy Cafe Production AI Gateway",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def correlation_trace_middleware(request: Request, call_next):
    """Injects and correlates X-Trace-ID across all requests and structured logs."""
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    request.state.trace_id = trace_id

    start_time = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    response.headers["X-Trace-ID"] = trace_id
    response.headers["X-Response-Time-Ms"] = str(duration_ms)

    # Emit structured request log
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)",
        extra={"trace_id": trace_id, "extra_data": {"duration_ms": duration_ms, "status": response.status_code}},
    )
    return response


# =============================================================================
# 4. HEALTH PROBE ENDPOINTS (KUBERNETES READY)
# =============================================================================
@app.get("/health/live", tags=["Observability"])
async def liveness_probe(request: Request):
    """
    Kubernetes Liveness Probe.
    Answers: 'Is the container alive or deadlock/crashed?'
    Returns 200 OK as long as the process loop is responsive.
    """
    if not getattr(request.app.state, "is_live", True):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "DEAD", "reason": "Process signaled unrecoverable state"},
        )
    uptime = round(time.time() - getattr(request.app.state, "startup_timestamp", APP_START_TIME), 2)
    return {
        "status": "ALIVE",
        "service": "cafe-production-gateway",
        "uptime_seconds": uptime,
    }


@app.get("/health/ready", tags=["Observability"])
async def readiness_probe(request: Request):
    """
    Kubernetes Readiness Probe.
    Answers: 'Is the application ready to receive production traffic?'
    Checks: DB connection pool, LLM client availability, application ready flag.
    """
    is_ready = getattr(request.app.state, "is_ready", False)
    db_healthy = False

    if hasattr(request.app.state, "db_pool"):
        db_healthy = await request.app.state.db_pool.ping()

    llm_available = hasattr(request.app.state, "llm") and request.app.state.llm is not None

    checks = {
        "database_pool": "HEALTHY" if db_healthy else "UNAVAILABLE",
        "llm_client": "READY" if llm_available else "NOT_INITIALIZED",
        "traffic_gate": "OPEN" if is_ready else "CLOSED",
    }

    if is_ready and db_healthy and llm_available:
        return {"status": "READY", "checks": checks}
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "NOT_READY", "checks": checks},
        )


# =============================================================================
# 5. BUSINESS DOMAIN ENDPOINTS
# =============================================================================
class RecommendationRequest(BaseModel):
    mood: str = Field(..., description="Customer's current vibe or preference")
    budget: float = Field(default=10.0, description="Customer budget in USD")


@app.post("/ai/recommend", tags=["AI Business Logic"])
async def get_beverage_recommendation(req: RecommendationRequest, request: Request):
    """Uses the pre-warmed lifespan LLM instance to generate a curated beverage match."""
    llm = request.app.state.llm
    prompt = (
        f"A customer at Cozy Cafe is feeling '{req.mood}' with a ${req.budget:.2f} budget. "
        "Recommend exactly one coffee drink and a one-sentence rationale. Be delightful."
    )
    result = await llm.ainvoke(prompt)
    return {
        "mood": req.mood,
        "recommendation": result.content.strip(),
        "served_by_model": ACTIVE_MODEL,
        "trace_id": getattr(request.state, "trace_id", "none"),
    }


# =============================================================================
# 6. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 035: PRODUCTION FASTAPI LIFESPAN, LOGGING & PROBES")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    # Running with TestClient as a context manager activates the lifespan startup & shutdown
    with TestClient(app) as client:
        print("\n" + "-" * 75)
        print("1. PROBING /health/live (Kubernetes Liveness Check)")
        print("-" * 75)
        res_live = client.get("/health/live")
        print(f"Status Code: {res_live.status_code}")
        print(f"Payload: {json.dumps(res_live.json(), indent=2)}")

        print("\n" + "-" * 75)
        print("2. PROBING /health/ready (Deep Subsystem Readiness Check)")
        print("-" * 75)
        res_ready = client.get("/health/ready")
        print(f"Status Code: {res_ready.status_code}")
        print(f"Payload: {json.dumps(res_ready.json(), indent=2)}")

        print("\n" + "-" * 75)
        print("3. INCOMING TRAFFIC: POST /ai/recommend (Trace ID Correlated)")
        print("-" * 75)
        req_headers = {"X-Trace-ID": "req-trace-cafe-9988"}
        res_rec = client.post(
            "/ai/recommend",
            json={"mood": "energetic and ready to code Python", "budget": 6.50},
            headers=req_headers,
        )
        print(f"Status Code: {res_rec.status_code}")
        print(f"Response Body: {json.dumps(res_rec.json(), indent=2)}")
        print(f"Response Header X-Trace-ID: {res_rec.headers.get('X-Trace-ID')}")
        print(f"Response Header X-Response-Time-Ms: {res_rec.headers.get('X-Response-Time-Ms')}ms")

    print("\n" + "-" * 75)
    print("4. LIFESPAN SHUTDOWN COMPLETE (Context manager exited cleanly)")
    print("-" * 75)
    print("[SUCCESS] Project 035 demonstration completed cleanly!")


if __name__ == "__main__":
    main()

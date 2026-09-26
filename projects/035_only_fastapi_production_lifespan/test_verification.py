"""
Test verification suite for Project 035: Production FastAPI Lifespan, Logging & Probes
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app


def test_lifespan_initialization_and_liveness():
    with TestClient(app) as client:
        # Check app.state initialized
        assert hasattr(app.state, "db_pool")
        assert hasattr(app.state, "llm")
        assert app.state.is_ready is True

        # Test liveness probe
        res_live = client.get("/health/live")
        assert res_live.status_code == 200
        data = res_live.json()
        assert data["status"] == "ALIVE"
        assert "uptime_seconds" in data


def test_readiness_probe_success():
    with TestClient(app) as client:
        res_ready = client.get("/health/ready")
        assert res_ready.status_code == 200
        data = res_ready.json()
        assert data["status"] == "READY"
        assert data["checks"]["database_pool"] == "HEALTHY"
        assert data["checks"]["llm_client"] == "READY"
        assert data["checks"]["traffic_gate"] == "OPEN"


def test_readiness_probe_degraded_state():
    with TestClient(app) as client:
        # Simulate degraded state
        app.state.is_ready = False
        res_ready = client.get("/health/ready")
        assert res_ready.status_code == 503
        data = res_ready.json()
        assert data["status"] == "NOT_READY"
        assert data["checks"]["traffic_gate"] == "CLOSED"

        # Restore ready state
        app.state.is_ready = True


def test_trace_middleware_headers():
    with TestClient(app) as client:
        custom_trace = "test-trace-12345"
        res = client.get("/health/live", headers={"X-Trace-ID": custom_trace})
        assert res.status_code == 200
        assert res.headers.get("X-Trace-ID") == custom_trace
        assert "X-Response-Time-Ms" in res.headers


def test_recommendation_endpoint():
    with TestClient(app) as client:
        res = client.post("/ai/recommend", json={"mood": "sleepy afternoon", "budget": 5.0})
        assert res.status_code == 200
        data = res.json()
        assert "recommendation" in data
        assert len(data["recommendation"]) > 0
        assert "trace_id" in data


def test_clean_shutdown():
    with TestClient(app) as client:
        assert app.state.db_pool.connected is True
    # Once context manager exits, shutdown was triggered
    assert app.state.db_pool.connected is False
    assert app.state.is_ready is False


if __name__ == "__main__":
    test_lifespan_initialization_and_liveness()
    test_readiness_probe_success()
    test_readiness_probe_degraded_state()
    test_trace_middleware_headers()
    test_recommendation_endpoint()
    test_clean_shutdown()
    print("Project 035: All verification tests PASSED successfully!")

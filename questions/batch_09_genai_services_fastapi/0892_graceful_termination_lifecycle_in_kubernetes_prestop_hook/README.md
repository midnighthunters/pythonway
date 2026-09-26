# Q0892 · Graceful termination lifecycle in Kubernetes: preStop hook and SIGTERM

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Hard |

## Question

Explain the exact Kubernetes pod shutdown lifecycle and write Python code handling SIGTERM to drain active SSE streaming connections before exiting.

## Answer

When a Kubernetes pod is deleted during a rolling deployment:
1. Pod state changes to `Terminating`; endpoint controller begins removing the pod IP from the Service's Endpoints.
2. A `preStop` hook executes (e.g. `sleep 10`) to allow iptables / kube-proxy updates to propagate across all nodes so no new traffic reaches the terminating pod.
3. The container receives `SIGTERM`. The application must stop accepting new requests, allow active streaming connections to finish (connection draining), and flush audit logs.
4. If the process does not exit within `terminationGracePeriodSeconds` (default 30s), Kubernetes issues `SIGKILL`.

```python
import asyncio
import signal


class GracefulServerManager:
    def __init__(self, draining_timeout_sec: float = 0.05):
        self.is_accepting_traffic = True
        self.active_connections = 0
        self.draining_timeout = draining_timeout_sec

    def handle_sigterm(self) -> None:
        # Step 1: Cease accepting new traffic
        self.is_accepting_traffic = False

    async def drain_active_connections(self) -> str:
        # Wait for active requests to finish or timeout
        start = asyncio.get_running_loop().time()
        while self.active_connections > 0:
            if (asyncio.get_running_loop().time() - start) > self.draining_timeout:
                return "TIMED_OUT_FORCED_EXIT"
            await asyncio.sleep(0.01)
        return "CLEAN_DRAIN_SUCCESS"


async def main():
    server = GracefulServerManager()
    server.active_connections = 2

    # Simulate SIGTERM arrival
    server.handle_sigterm()
    assert server.is_accepting_traffic is False

    # Simulate in-flight requests completing
    async def finish_requests():
        await asyncio.sleep(0.02)
        server.active_connections = 0

    asyncio.create_task(finish_requests())
    status = await server.drain_active_connections()
    assert status == "CLEAN_DRAIN_SUCCESS"


asyncio.run(main())
```

## Likely follow-ups

- Why is `preStop: exec: command: ["/bin/sh", "-c", "sleep 10"]` essential before SIGTERM?
- How do you configure Uvicorn's `--timeout-graceful-shutdown` parameter?

---

[← Q0891](../../batch_09_genai_services_fastapi/0891_keda_scaled_object_based_on_redis_queue_depth/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0893 →](../../batch_09_genai_services_fastapi/0893_rolling_zero_downtime_deployments_and_blue_green_canary/README.md)

# Q0887 · Uvicorn vs Gunicorn architecture and worker count calculation

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Explain the relationship between Gunicorn (master process manager) and Uvicorn (`UvicornWorker`), and write Python code calculating optimal worker process counts based on CPU and I/O characteristics.

## Answer

- **Uvicorn**: High-performance ASGI server built on `uvloop` and `httptools`. Handles async I/O efficiently within a single process.
- **Gunicorn**: Production WSGI process manager. It monitors worker processes, gracefully handles restarts upon crashes, reloads workers without downtime, and distributes incoming socket connections.
- **Combined Pattern**: `gunicorn -k uvicorn.workers.UvicornWorker main:app`.

```python
def calculate_optimal_workers(cpu_cores: int, workload_type: str = "io_bound") -> int:
    '''Calculates recommended worker process count for Gunicorn / Uvicorn.'''
    if workload_type == "cpu_bound":
        # CPU-heavy tasks (e.g. local ONNX embeddings or text chunking)
        return max(1, cpu_cores)
    elif workload_type == "io_bound":
        # Async I/O heavy (FastAPI calling cloud APIs and databases)
        # Standard production formula: 2 * cores + 1
        return (2 * cpu_cores) + 1
    elif workload_type == "container_k8s":
        # Inside Kubernetes pods, standard practice is 1-2 workers per pod to allow K8s HPA to scale pods
        return min(2, cpu_cores)
    return 2


# 4-core virtual machine running async I/O FastAPI
assert calculate_optimal_workers(cpu_cores=4, workload_type="io_bound") == 9

# Kubernetes pod with 2 vCPU limit
assert calculate_optimal_workers(cpu_cores=2, workload_type="container_k8s") == 2
```

## Likely follow-ups

- Why is running 1 or 2 workers per Kubernetes pod often preferred over running 16 workers in a giant pod?
- What happens if an unhandled exception causes a worker to exit when running standalone Uvicorn vs Gunicorn?

---

[← Q0886](../../batch_09_genai_services_fastapi/0886_multi_stage_dockerfile_for_fastapi_genai_microservices_with/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0888 →](../../batch_09_genai_services_fastapi/0888_uvicorn_loop_optimization_with_uvloop_and_httptools_in/README.md)

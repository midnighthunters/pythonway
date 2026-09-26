# Q0886 · Multi-stage Dockerfile for FastAPI GenAI microservices with non-root security

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Write a production-grade multi-stage Dockerfile for a Python FastAPI GenAI microservice, including non-root user security, dependency caching, and minimal attack surface.

## Answer

In enterprise banking, container images must adhere to strict cybersecurity standards:
1. Multi-stage builds to keep build tools (gcc, g++, git) out of the final runtime image.
2. Running as an unprivileged non-root user (UID 10001).
3. Utilizing a slim or distroless base image to reduce CVE vulnerabilities.
4. Setting optimal Python environment flags (`PYTHONUNBUFFERED=1`, `PYTHONDONTWRITEBYTECODE=1`).

```python
# no-run
# Production Multi-Stage Dockerfile
DOCKERFILE = '''
# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final minimal runtime image
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /app

# Create unprivileged application user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/bash -m appuser

# Copy installed Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/livez || exit 1

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
```

## Likely follow-ups

- Why should secrets and credentials never be baked into Docker image layers or environment variables?
- What are the advantages of Chainguard or Google Distroless base images over Debian-slim?

---

[← Q0885](../../batch_09_genai_services_fastapi/0885_testing_async_workers_in_isolation_with_mocks_and_test/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0887 →](../../batch_09_genai_services_fastapi/0887_uvicorn_vs_gunicorn_architecture_and_worker_count/README.md)

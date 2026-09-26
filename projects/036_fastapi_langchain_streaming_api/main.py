"""
===============================================================================
PROJECT 036: FASTAPI + LANGCHAIN: TOKEN STREAMING API & RUN TELEMETRY
Stage 2: Pairwise Combos | Difficulty: 4.0 / 10
===============================================================================

THE BIG QUESTION:
How do production conversational services stream LLM tokens to client browsers
in real time while tracking exact generation telemetry (time-to-first-token,
throughput, run lineage) compatible with observability systems like LangSmith?

ARCHITECTURE:
1. LCEL Chain: ChatPromptTemplate | ChatGroq(streaming=True) | StrOutputParser
2. Custom LangSmith-Style Async Callback: Captures TTFT & token count.
3. Server-Sent Events (SSE) Endpoint: /chat/stream via FastAPI StreamingResponse.
4. Run Telemetry Ledger: In-memory store of run IDs, tokens, and latencies.
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
import asyncio
from typing import Dict, Any, List, Optional, AsyncIterator
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks.base import AsyncCallbackHandler
from langchain_core.outputs import LLMResult

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. RUN TELEMETRY & LANGSMITH-COMPATIBLE CALLBACK HANDLER
# =============================================================================
RUN_TELEMETRY_STORE: Dict[str, Dict[str, Any]] = {}


class LangSmithStreamTracker(AsyncCallbackHandler):
    """
    Asynchronous callback handler simulating LangSmith run tracing.
    Calculates Time-To-First-Token (TTFT), tokens generated, and total latency.
    """

    def __init__(self, run_id: str, tags: List[str], metadata: Dict[str, Any]):
        super().__init__()
        self.run_id = run_id
        self.tags = tags
        self.metadata = metadata
        self.start_time = 0.0
        self.first_token_time: Optional[float] = None
        self.end_time = 0.0
        self.token_count = 0

    async def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        self.start_time = time.perf_counter()
        RUN_TELEMETRY_STORE[self.run_id] = {
            "run_id": self.run_id,
            "status": "RUNNING",
            "model": ACTIVE_MODEL,
            "tags": self.tags,
            "metadata": self.metadata,
            "token_count": 0,
            "ttft_ms": None,
            "total_latency_ms": None,
        }

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.token_count += 1
        if self.first_token_time is None:
            self.first_token_time = time.perf_counter()

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.end_time = time.perf_counter()
        ttft_ms = round((self.first_token_time - self.start_time) * 1000, 2) if self.first_token_time else 0.0
        total_ms = round((self.end_time - self.start_time) * 1000, 2)
        tokens_per_sec = round(self.token_count / (total_ms / 1000), 1) if total_ms > 0 else 0.0

        RUN_TELEMETRY_STORE[self.run_id].update({
            "status": "COMPLETED",
            "token_count": self.token_count,
            "ttft_ms": ttft_ms,
            "total_latency_ms": total_ms,
            "tokens_per_sec": tokens_per_sec,
        })


# =============================================================================
# 2. LCEL PIPELINE FACTORY
# =============================================================================
def build_barista_chain():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an artisanal barista master at Cozy Cafe. "
            "Provide insightful, friendly coffee advice in 2-3 concise sentences.",
        ),
        ("human", "{query}"),
    ])
    llm = get_llm(temperature=0.2)
    parser = StrOutputParser()
    return prompt | llm | parser


# =============================================================================
# 3. FASTAPI APPLICATION & SSE STREAMING
# =============================================================================
app = FastAPI(title="FastAPI + LangChain Streaming Gateway", version="1.0.0")


class StreamQueryRequest(BaseModel):
    query: str = Field(..., description="Customer coffee question")
    user_id: str = Field(default="guest-1", description="Client user ID")
    tags: List[str] = Field(default_factory=lambda: ["production", "cafe-chat"])


@app.post("/chat/stream")
async def chat_stream_endpoint(req: StreamQueryRequest):
    """
    Streams LangChain LCEL tokens using Server-Sent Events (SSE).
    Emits token events, followed by telemetry event and final done event.
    """
    run_id = f"run_{uuid.uuid4().hex[:12]}"
    chain = build_barista_chain()
    tracker = LangSmithStreamTracker(
        run_id=run_id,
        tags=req.tags,
        metadata={"user_id": req.user_id, "endpoint": "/chat/stream"},
    )

    async def sse_event_generator() -> AsyncIterator[str]:
        # 1. Initial event: metadata
        initial_event = {
            "type": "metadata",
            "run_id": run_id,
            "model": ACTIVE_MODEL,
        }
        yield f"data: {json.dumps(initial_event)}\n\n"

        # 2. Token chunks from LCEL astream()
        try:
            async for chunk in chain.astream(
                {"query": req.query},
                config={"callbacks": [tracker], "run_name": "CozyBaristaStream"},
            ):
                token_event = {"type": "token", "content": chunk}
                yield f"data: {json.dumps(token_event)}\n\n"
        except Exception as exc:
            err_event = {"type": "error", "detail": str(exc)}
            yield f"data: {json.dumps(err_event)}\n\n"
            return

        # 3. Completion telemetry event
        telemetry = RUN_TELEMETRY_STORE.get(run_id, {})
        final_event = {
            "type": "telemetry",
            "run_id": run_id,
            "metrics": telemetry,
        }
        yield f"data: {json.dumps(final_event)}\n\n"

        # 4. Standard SSE terminal event
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(sse_event_generator(), media_type="text/event-stream")


@app.get("/telemetry/runs")
def get_runs_telemetry():
    """Returns LangSmith-style run metrics for past executions."""
    return {"total_runs": len(RUN_TELEMETRY_STORE), "runs": list(RUN_TELEMETRY_STORE.values())}


# =============================================================================
# 4. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 036: FASTAPI + LANGCHAIN SSE STREAMING & TELEMETRY")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    client = TestClient(app)
    query = "What is the key difference between a Cortado and a Flat White?"

    print(f"\nSubmitting Query: '{query}'")
    print("-" * 75)
    print("Receiving Live SSE Token Stream:")
    print("-" * 75)

    run_id = None
    streamed_text = []

    with client.stream("POST", "/chat/stream", json={"query": query, "user_id": "vip-alice"}) as response:
        for line in response.iter_lines():
            if not line:
                continue
            if line.startswith("data: "):
                payload_str = line[6:]
                if payload_str == "[DONE]":
                    print("\n[STREAM EVENT: DONE]")
                    break
                payload = json.loads(payload_str)
                event_type = payload.get("type")

                if event_type == "metadata":
                    run_id = payload.get("run_id")
                    print(f"[RUN CREATED] ID: {run_id} | Model: {payload.get('model')}")
                    print("Stream Output: ", end="", flush=True)
                elif event_type == "token":
                    content = payload.get("content", "")
                    streamed_text.append(content)
                    print(content, end="", flush=True)
                elif event_type == "telemetry":
                    metrics = payload.get("metrics", {})
                    print(f"\n\n[TELEMETRY SUMMARY]")
                    print(f"- Run ID: {metrics.get('run_id')}")
                    print(f"- Time to First Token (TTFT): {metrics.get('ttft_ms')} ms")
                    print(f"- Total Latency: {metrics.get('total_latency_ms')} ms")
                    print(f"- Total Tokens: {metrics.get('token_count')}")
                    print(f"- Generation Speed: {metrics.get('tokens_per_sec')} tokens/sec")

    # Fetch recorded run telemetry from observability endpoint
    print("\n" + "-" * 75)
    print("Inspecting Run Registry: GET /telemetry/runs")
    print("-" * 75)
    runs_res = client.get("/telemetry/runs")
    print(json.dumps(runs_res.json(), indent=2))

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 036 demonstration completed cleanly!")


if __name__ == "__main__":
    main()

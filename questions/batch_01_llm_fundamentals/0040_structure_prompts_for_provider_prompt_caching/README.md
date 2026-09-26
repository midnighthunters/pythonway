# Q0040 · Structure prompts for provider prompt caching

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Cost optimisation | Medium |

## Question

Providers discount repeated prompt prefixes (prompt caching). Write a function that orders prompt sections into a static prefix and dynamic suffix, and compute the savings for a workload given a cache discount.

## Answer

Why it matters here: on a platform serving many users with the same system prompt, tool definitions and policy documents, cache-friendly prompt layout is one of the cheapest cost and TTFT wins.

Rules: caching matches exact token prefixes. Put stable content first (system instructions, tool schemas, few-shot examples, large reference documents) and variable content last (retrieved chunks, user message). Keep the stable parts byte-identical: no timestamps, request ids or reordered tool lists up front. Some providers cache automatically above a minimum length, and others require explicit cache breakpoints. Check each provider's rules and TTLs.

```python
from decimal import Decimal


def build_prompt(sections: list[dict]) -> tuple[str, int]:
    """sections: {'text': str, 'static': bool}. Returns prompt and length of the static prefix."""
    static = [s["text"] for s in sections if s["static"]]
    dynamic = [s["text"] for s in sections if not s["static"]]
    prefix = "\n\n".join(static)
    prompt = prefix + ("\n\n" if static and dynamic else "") + "\n\n".join(dynamic)
    return prompt, len(prefix)


def cached_cost(requests: int, prefix_tokens: int, suffix_tokens: int, price_per_m: Decimal,
                cache_discount: Decimal, hit_rate: Decimal) -> tuple[Decimal, Decimal]:
    full = requests * (prefix_tokens + suffix_tokens) * price_per_m / 1_000_000
    hits = requests * hit_rate
    saved = hits * prefix_tokens * price_per_m * cache_discount / 1_000_000
    return full, full - saved


prompt, n = build_prompt([
    {"text": "USER: What is our travel policy?", "static": False},
    {"text": "SYSTEM: You are the LLM Suite assistant.", "static": True},
    {"text": "TOOLS: search_policies(query)", "static": True},
])
assert prompt.startswith("SYSTEM") and prompt.endswith("travel policy?") and prompt[:n].endswith("query)")
full, with_cache = cached_cost(100_000, 6_000, 500, Decimal("2.50"), Decimal("0.90"), Decimal("0.8"))
assert full == Decimal("1625") and with_cache == Decimal("545")
```

The prices and discount are illustrative. With a 6k-token stable prefix and an 80% hit rate, input cost falls by about two-thirds.

## Likely follow-ups

- What silently breaks cache hits (a timestamp in the system prompt, non-deterministic tool ordering)?
- How does the MCP 2026-07-28 guidance on deterministic `tools/list` ordering help prompt caching?

---

[← Q0039](../../batch_01_llm_fundamentals/0039_pagedattention_and_vllm/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0041 →](../../batch_01_llm_fundamentals/0041_mixture_of_experts_routing/README.md)

"""
===============================================================================
PROJECT 005: RESILIENT CHAINS: FALLBACKS, RETRIES & OBSERVABILITY
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

Core Concepts Demonstrated:
1. Model-Level Fallbacks: with_fallbacks([backup_model_1, backup_model_2]).
2. Exponential Backoff Retries: with_retry(stop_after_attempt=3).
3. Chain-Level Fallback Routing: Recovering gracefully from parsing errors.
4. LangSmith Observability: Tracing fallback switches and latency profiling.
===============================================================================
"""

import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from config import get_llm, ACTIVE_MODEL


def demo_model_fallback():
    """Step 1: Demonstrates automatic routing to a backup model when the primary model fails."""
    print("=" * 70)
    print("STEP 1: AUTOMATIC MODEL FALLBACK (with_fallbacks)")
    print("=" * 70)
    print("In production, providers experience outages or 429 rate limits.")
    print("with_fallbacks seamlessly switches to an alternate model without downtime.\n")

    # Intentionally configure an invalid primary model that is guaranteed to fail
    failing_primary_model = get_llm(model="non-existent-broken-model-v99")

    # Reliable backup model
    reliable_backup_model = get_llm(model=ACTIVE_MODEL, temperature=0.0)

    # Attach fallback
    resilient_llm = failing_primary_model.with_fallbacks([reliable_backup_model])

    prompt = ChatPromptTemplate.from_template("What is 10 + 25? Reply with only the single number.")
    chain = prompt | resilient_llm | StrOutputParser()

    print("Attempting invocation...")
    print(" [Notice]: Primary model 'non-existent-broken-model-v99' will fail.")
    print(f" [Notice]: Chain will automatically fall back to '{ACTIVE_MODEL}'.\n")

    t0 = time.time()
    result = chain.invoke({}, config={"tags": ["project-005", "model-fallback-test"]})
    elapsed = time.time() - t0

    print(f"Execution Succeeded via Fallback in {elapsed:.2f}s!")
    print(f"Result: {result.strip()}")
    print("-" * 70)


def demo_retry_mechanism():
    """Step 2: Demonstrates automatic retry on transient exceptions."""
    print("\n" + "=" * 70)
    print("STEP 2: EXPONENTIAL BACKOFF RETRIES (.with_retry())")
    print("=" * 70)
    print("Automatically retries transient network blips up to N times.\n")

    attempts = {"count": 0}

    # A simulated flaky API function that fails twice before succeeding on attempt 3
    def flaky_network_call(payload):
        attempts["count"] += 1
        print(f"   [Flaky API Attempt {attempts['count']}] Connecting...")
        if attempts["count"] < 3:
            raise ConnectionResetError(f"Transient 503 Service Unavailable (Attempt {attempts['count']})")
        return f"Successfully retrieved data on attempt {attempts['count']}!"

    runnable_flaky = RunnableLambda(flaky_network_call).with_retry(
        stop_after_attempt=4,
        wait_exponential_jitter=False,
    )

    print("Triggering runnable configured with .with_retry(stop_after_attempt=4):")
    res = runnable_flaky.invoke({"query": "fetch_record"})
    print(f"\nFinal Outcome: {res}")
    print("-" * 70)


def demo_chain_level_fallback():
    """Step 3: Demonstrates recovering from complex pipeline failures."""
    print("\n" + "=" * 70)
    print("STEP 3: CHAIN-LEVEL FALLBACK (Primary Pipeline -> Safe Default)")
    print("=" * 70)
    print("If an advanced analysis chain errors, catch it and return a safe recovery response.\n")

    # Primary complex chain that might fail on malformed inputs
    def strict_parser(text):
        if "ERROR" in text:
            raise ValueError("Data parse failure: Malformed response")
        return f"PARSED: {text}"

    fragile_chain = (
        ChatPromptTemplate.from_template("Generate raw unformatted text: {input}")
        | get_llm()
        | StrOutputParser()
        | RunnableLambda(strict_parser)
    )

    # Safe fallback chain that always succeeds
    safe_fallback_chain = RunnableLambda(
        lambda x: "RECOVERY_ALERT: Primary pipeline failed. Returned safe static fallback response."
    )

    resilient_pipeline = fragile_chain.with_fallbacks([safe_fallback_chain])

    print("Running chain with intentional failure...")
    output = resilient_pipeline.invoke({"input": "ERROR: cause strict parser to fail"})
    print(f"Pipeline Result:\n{output}")
    print("=" * 70)


def main():
    print("*" * 70)
    print("PROJECT 005: RESILIENT CHAINS: FALLBACKS, RETRIES & OBSERVABILITY")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    demo_model_fallback()
    demo_retry_mechanism()
    demo_chain_level_fallback()
    print("\n[SUCCESS] Project 005 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()

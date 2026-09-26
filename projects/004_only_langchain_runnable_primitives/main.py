"""
===============================================================================
PROJECT 004: ADVANCED LCEL: RUNNABLEPARALLEL, PASSTHROUGH & LAMBDAS
Stage 1: Pure Fundamentals | Difficulty: 2.5 / 10 (Intermediate)
===============================================================================

Core Concepts Demonstrated:
1. RunnableParallel: Executing multi-branch LLM analyses concurrently.
2. RunnablePassthrough: Forwarding input parameters down the DAG unmodified.
3. RunnablePassthrough.assign(): Dynamically adding new keys to the state dict mid-chain.
4. RunnableLambda: Wrapping custom Python transformation functions as native Runnables.
===============================================================================
"""

import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from config import get_llm, ACTIVE_MODEL


def demo_parallel_triad_evaluation():
    """Step 1: Demonstrates concurrent multi-perspective evaluation."""
    print("=" * 70)
    print("STEP 1: MULTI-PERSPECTIVE EVALUATION VIA RUNNABLEPARALLEL")
    print("=" * 70)
    print("Evaluates a technical proposal from 3 distinct angles concurrently:")
    print("  - Branch A: Security & Compliance Auditor")
    print("  - Branch B: Cloud FinOps & Infrastructure Cost Estimator")
    print("  - Branch C: Developer Velocity & Maintainability Specialist\n")

    llm = get_llm(temperature=0.2)

    # 1. Branch A: Security
    security_chain = (
        ChatPromptTemplate.from_template(
            "You are a Chief Information Security Officer (CISO). Identify the #1 top security risk of:\n'{proposal}'.\n"
            "State the risk in 1 concise sentence."
        )
        | llm
        | StrOutputParser()
    )

    # 2. Branch B: FinOps / Cost
    cost_chain = (
        ChatPromptTemplate.from_template(
            "You are a Cloud FinOps Architect. Estimate the financial cost impact of:\n'{proposal}'.\n"
            "State the cost factor in 1 concise sentence."
        )
        | llm
        | StrOutputParser()
    )

    # 3. Branch C: Velocity
    velocity_chain = (
        ChatPromptTemplate.from_template(
            "You are a VP of Engineering. Evaluate developer velocity impact of:\n'{proposal}'.\n"
            "State velocity impact in 1 concise sentence."
        )
        | llm
        | StrOutputParser()
    )

    # Combine into RunnableParallel
    parallel_review_board = RunnableParallel(
        security=security_chain,
        cost=cost_chain,
        velocity=velocity_chain,
        proposal=RunnablePassthrough(),  # Preserves the proposal string!
    )

    sample_proposal = (
        "Migrating all user session storage from Redis to an in-memory decentralized browser SQLite database."
    )

    print(f"Submitting Proposal: '{sample_proposal}'\n")
    t0 = time.time()
    evaluation_results = parallel_review_board.invoke(sample_proposal)
    elapsed = time.time() - t0

    print(f"Parallel Evaluation completed in {elapsed:.2f}s:")
    print(f" - Security Risk : {evaluation_results['security']}")
    print(f" - FinOps Cost   : {evaluation_results['cost']}")
    print(f" - Dev Velocity  : {evaluation_results['velocity']}")
    print("-" * 70)
    return evaluation_results


def demo_passthrough_assign_and_lambdas(eval_data):
    """Step 2: Demonstrates RunnablePassthrough.assign() and custom RunnableLambdas."""
    print("\n" + "=" * 70)
    print("STEP 2: RUNNABLEPASSTHROUGH.ASSIGN() & RUNNABLELAMBDA")
    print("=" * 70)
    print("Extends existing dictionaries mid-chain and transforms content using Python lambdas.\n")

    llm = get_llm(temperature=0.3)

    # RunnableLambda to calculate word metrics
    calculate_risk_weight = RunnableLambda(
        lambda data: "HIGH" if "risk" in data["security"].lower() or "vulnerability" in data["security"].lower() else "MEDIUM"
    )

    # Synthesizer prompt that consumes all parallel outputs
    synthesis_prompt = ChatPromptTemplate.from_template(
        "Proposal: {proposal}\n\n"
        "Security Assessment: {security}\n"
        "FinOps Assessment: {cost}\n"
        "Velocity Assessment: {velocity}\n"
        "Assigned Risk Tier: {risk_tier}\n\n"
        "As Chief Technology Officer (CTO), provide a 2-sentence executive decision on whether to proceed."
    )

    # Chain using RunnablePassthrough.assign to inject 'risk_tier' dynamically
    executive_decision_chain = (
        RunnablePassthrough.assign(risk_tier=calculate_risk_weight)
        | synthesis_prompt
        | llm
        | StrOutputParser()
    )

    print("Running CTO Synthesis Chain...")
    decision = executive_decision_chain.invoke(eval_data)

    print(f"\n[FINAL CTO EXECUTIVE MEMO]:\n{decision}")
    print("=" * 70)


def main():
    print("*" * 70)
    print("PROJECT 004: ADVANCED LCEL: RUNNABLEPARALLEL & PASSTHROUGH")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    eval_data = demo_parallel_triad_evaluation()
    demo_passthrough_assign_and_lambdas(eval_data)
    print("\n[SUCCESS] Project 004 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()

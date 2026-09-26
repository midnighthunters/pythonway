"""
===============================================================================
PROJECT 001: HELLO LCEL: CHAT MODELS, MESSAGES & UNIX PIPES
Stage 1: Pure Fundamentals | Difficulty: 1.0 / 10 (Beginner)
===============================================================================

Core Concepts Demonstrated:
1. Message Types: SystemMessage, HumanMessage, AIMessage.
2. LCEL Composition: pipe syntax (prompt | model | parser).
3. StrOutputParser: Extracting clean string responses from AIMessage objects.
4. Invocation Protocols: .invoke(), .stream(), and .batch().
5. LangSmith Tracing: Attaching metadata and tags to run configurations.
===============================================================================
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_llm, ACTIVE_MODEL


def demo_raw_messages():
    """Step 1: Demonstrates passing structured message objects directly to the model."""
    print("=" * 70)
    print("STEP 1: RAW CHAT MESSAGES (SystemMessage, HumanMessage, AIMessage)")
    print("=" * 70)
    print("Models accept structured messages defining roles:")
    print(" - SystemMessage: Sets the operational persona and boundaries.")
    print(" - HumanMessage: The user prompt or instruction.")
    print(" - AIMessage: The assistant's prior answers for conversation history.\n")

    llm = get_llm(temperature=0.2)

    conversation = [
        SystemMessage(content="You are a concise Unix systems engineer. Answer in 2 lines."),
        HumanMessage(content="What command displays current memory usage in human-readable format?"),
    ]

    print("Sending conversation to model...")
    response = llm.invoke(conversation)

    print(f"Assistant Output ({type(response).__name__}):")
    print(response.content)
    print("-" * 70)


def demo_lcel_pipe():
    """Step 2: Demonstrates LangChain Expression Language (LCEL) Unix pipe syntax."""
    print("\n" + "=" * 70)
    print("STEP 2: LCEL PIPE SYNTAX (prompt | model | parser)")
    print("=" * 70)
    print("In LCEL, the '|' operator chains Runnables together declaratively:")
    print("  Input Dict -> ChatPromptTemplate -> ChatGroq -> StrOutputParser -> String\n")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional translator. Translate the text to {language}."),
        ("human", "{text}"),
    ])
    llm = get_llm(temperature=0.0)
    parser = StrOutputParser()

    # The LCEL Chain
    chain = prompt | llm | parser

    # Invoke with LangSmith tags & metadata
    run_config = {
        "tags": ["project-001", "hello-lcel", "translation"],
        "metadata": {"user_level": "beginner", "difficulty": "1.0"},
    }

    input_payload = {
        "language": "Japanese (Polite / Keigo)",
        "text": "Hello, thank you for meeting with us today.",
    }

    print(f"Translating: '{input_payload['text']}' into {input_payload['language']}...")
    result = chain.invoke(input_payload, config=run_config)
    print(f"Result:\n{result}")
    print("-" * 70)


def demo_streaming_and_batching():
    """Step 3: Demonstrates streaming tokens live and executing concurrent batches."""
    print("\n" + "=" * 70)
    print("STEP 3: STREAMING (.stream()) & BATCHING (.batch())")
    print("=" * 70)

    prompt = ChatPromptTemplate.from_template(
        "Write an exhaustive, comprehensive, in-depth technical treatise on '{term}' "
        "of at least 2000 words. Cover its historical origins, rigorous mathematical formulations, "
        "architectural variants, activation functions, backpropagation and optimization dynamics, "
        "regularization methods, distributed training considerations, and future horizons. "
        "Be extremely detailed, thorough, and analytical."
    )
    llm = get_llm(temperature=0.7, max_tokens=3500)
    chain = prompt | llm | StrOutputParser()

    # 1. LIVE TOKEN STREAMING
    print("[1. LIVE STREAMING TOKENS (Large Generation ~2000+ Tokens)]:\n")
    chunk_count = 0
    for chunk in chain.stream({"term": "The Architecture and Mathematics of Deep Neural Networks"}):
        print(chunk, end="", flush=True)
        chunk_count += 1
    print(f"\n\n[Finished streaming. Total chunks received: {chunk_count}]\n")

    # 2. CONCURRENT BATCH EXECUTION
    print("[2. CONCURRENT BATCH EXECUTION]:")
    terms = [
        {"term": "Gradient Descent"},
        {"term": "Backpropagation"},
    ]
    results = chain.batch(terms)
    for t, r in zip(terms, results):
        print(f" - {t['term']}: {r.strip()}")
    print("=" * 70)


def main():
    print("*" * 70)
    print("PROJECT 001: HELLO LCEL: CHAT MODELS, MESSAGES & UNIX PIPES")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    # demo_raw_messages()
    # demo_lcel_pipe()
    demo_streaming_and_batching()
    print("\n[SUCCESS] Project 001 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()

"""
===============================================================================
LANGCHAIN CONCEPT 1: CHAT MODELS, MESSAGES, AND PROMPT TEMPLATES
===============================================================================

What is LangChain?
-----------------
LangChain is a framework for developing applications powered by large language models.
While LangGraph handles stateful, cyclical multi-actor graphs,
LangChain provides the foundational primitives for:
  - Chat Models & Messaging abstractions
  - Prompt Templates & Dynamic Variable Injection
  - Composable Chains (via LangChain Expression Language / LCEL)
  - Retrieval-Augmented Generation (RAG)
  - Tool execution & Structured Outputs

In this lesson:
  1. Working with Message types: SystemMessage, HumanMessage, AIMessage.
  2. Building dynamic ChatPromptTemplates with variable placeholders.
  3. Composing a basic LCEL chain: `prompt | llm | StrOutputParser()`.
  4. Real-time streaming (`chain.stream(...)`).
  5. High-throughput batch processing (`chain.batch(...)`).
===============================================================================
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. MESSAGE ABSTRACTIONS
# =============================================================================
def demo_messages():
    print("=" * 70)
    print("PART 1: CHAT MESSAGES (System, Human, AI)")
    print("=" * 70)
    print("LangChain models accept a list of structured message objects:")
    print(" - SystemMessage: Sets the persona and operational boundaries.")
    print(" - HumanMessage: The user's query or instruction.")
    print(" - AIMessage: The assistant's previous responses (for conversation history).\n")

    llm = get_llm(temperature=0.3)

    messages = [
        SystemMessage(content="You are a poetic Unix terminal assistant. Answer in 2 lines."),
        HumanMessage(content="How do I find all files ending in .py in the current directory?"),
    ]

    response = llm.invoke(messages)
    print("User Query: How do I find all files ending in .py?")
    print(f"Assistant ({type(response).__name__}):\n{response.content}\n")


# =============================================================================
# 2. PROMPT TEMPLATES
# =============================================================================
def demo_prompt_templates():
    print("=" * 70)
    print("PART 2: DYNAMIC CHAT PROMPT TEMPLATES")
    print("=" * 70)
    print("ChatPromptTemplate allows parameterized prompts without fragile f-strings.\n")

    # Define template with placeholders: {audience} and {topic}
    prompt_template = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert science communicator. Explain the given topic "
            "so it is perfectly understood by the specified audience in 2 concise sentences."
        ),
        (
            "human",
            "Audience: {audience}\nTopic: {topic}"
        ),
    ])

    llm = get_llm(temperature=0.4)
    # StrOutputParser converts the AIMessage object into a clean Python string
    parser = StrOutputParser()

    # LCEL (LangChain Expression Language) Composition:
    # prompt | model | parser
    chain = prompt_template | llm | parser

    # Invoke with parameters
    result = chain.invoke({
        "audience": "a 10-year-old child",
        "topic": "Quantum Entanglement",
    })

    print("Explanation for a 10-year-old:")
    print(result)


# =============================================================================
# 3. STREAMING AND BATCHING
# =============================================================================
def demo_streaming_and_batching():
    print("\n" + "=" * 70)
    print("PART 3: STREAMING & BATCHING WITH LCEL")
    print("=" * 70)

    prompt = ChatPromptTemplate.from_template("Translate this phrase to French, German, and Spanish: '{phrase}'")
    llm = get_llm(temperature=0.0)
    chain = prompt | llm | StrOutputParser()

    # 1. STREAMING: Stream tokens chunk-by-chunk as they arrive from Groq
    print("[1. LIVE STREAMING TOKENS]:")
    print("Translating 'Good morning, how are you today?' ->\n")
    for chunk in chain.stream({"phrase": "Good morning, how are you today?"}):
        print(chunk, end="", flush=True)
    print("\n")

    # 2. BATCHING: Send multiple inputs concurrently through the same chain
    print("-" * 50)
    print("[2. CONCURRENT BATCH EXECUTION]:")
    phrases = [
        {"phrase": "Thank you very much"},
        {"phrase": "Where is the train station?"},
    ]
    results = chain.batch(phrases)
    for idx, (p, r) in enumerate(zip(phrases, results), 1):
        print(f"\nBatch Item {idx} ('{p['phrase']}'):\n{r}")


# =============================================================================
# MAIN RUNNER
# =============================================================================
def main():
    print("=" * 70)
    print("LANGCHAIN LESSON 1: PROMPTS, MODELS, STREAMING & BATCHING")
    print(f"Provider: Groq | Model: {ACTIVE_MODEL}")
    print("=" * 70)

    demo_messages()
    demo_prompt_templates()
    demo_streaming_and_batching()


if __name__ == "__main__":
    main()

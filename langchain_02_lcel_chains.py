"""
===============================================================================
LANGCHAIN CONCEPT 2: LCEL (LANGCHAIN EXPRESSION LANGUAGE) & CHAINS
===============================================================================

What is LCEL?
-------------
LangChain Expression Language (LCEL) is a declarative way to compose chains
using the Unix-style pipe operator `|`.

Every LCEL component is a `Runnable` supporting:
  - `.invoke()`: Single input -> single output
  - `.stream()`: Real-time token streaming
  - `.batch()`: Parallel batch evaluation
  - `.ainvoke()`: Asynchronous execution

Key primitives covered:
  1. Sequential Chaining: `component_A | component_B | component_C`
  2. Parallel Execution (`RunnableParallel` / dict syntax):
     Run multiple chains concurrently on the same input.
  3. `RunnablePassthrough`: Pass inputs down the chain without modification.
  4. `RunnableLambda`: Inject custom Python functions seamlessly into LCEL.
===============================================================================
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from config import get_llm


# =============================================================================
# 1. SEQUENTIAL LCEL CHAIN
# =============================================================================
def demo_sequential_chain():
    print("=" * 70)
    print("PART 1: SEQUENTIAL CHAINING (Pipe Operator |)")
    print("=" * 70)
    print("Flow: Raw Text -> Summarize -> Translate to Spanish -> UpperCase\n")

    llm = get_llm(temperature=0.0)

    # Step 1: Summarize text into 1 sentence
    prompt_summarize = ChatPromptTemplate.from_template(
        "Summarize this text in exactly one concise sentence:\n'{text}'"
    )

    # Step 2: Translate summary into Spanish
    prompt_translate = ChatPromptTemplate.from_template(
        "Translate this sentence into Spanish:\n'{summary}'"
    )

    # Step 3: Custom Python transformation using RunnableLambda
    to_uppercase = RunnableLambda(lambda text: text.upper())

    # Build the sequential pipeline:
    # 1. Take input dict {"text": "..."}
    # 2. Run through summarize prompt -> LLM -> StrOutputParser
    # 3. Format into {"summary": summary_string}
    # 4. Run through translate prompt -> LLM -> StrOutputParser
    # 5. Transform to uppercase
    chain = (
        prompt_summarize
        | llm
        | StrOutputParser()
        | (lambda summary: {"summary": summary})
        | prompt_translate
        | llm
        | StrOutputParser()
        | to_uppercase
    )

    sample_article = (
        "Electric vehicles have experienced massive global adoption over the last decade, "
        "driven by battery advancements, governmental subsidies, and growing environmental "
        "concerns. However, grid infrastructure challenges and raw mineral supply chains "
        "remain key hurdles for future universal transition."
    )

    print("Executing sequential chain...")
    result = chain.invoke({"text": sample_article})
    print(f"\nFinal Result (Spanish & Uppercase):\n{result}\n")


# =============================================================================
# 2. PARALLEL EXECUTION WITH RUNNABLEPARALLEL
# =============================================================================
def demo_parallel_chains():
    print("=" * 70)
    print("PART 2: RUNNABLEPARALLEL (CONCURRENT MULTI-BRANCH EVALUATION)")
    print("=" * 70)
    print("Given a proposal, evaluate 'Pros' and 'Cons' in parallel, then synthesize a verdict.\n")

    llm = get_llm(temperature=0.3)

    # Branch A: Pros
    pros_chain = (
        ChatPromptTemplate.from_template("List 2 strong advantages of: {proposal}. Be very concise.")
        | llm
        | StrOutputParser()
    )

    # Branch B: Cons
    cons_chain = (
        ChatPromptTemplate.from_template("List 2 serious risks/disadvantages of: {proposal}. Be very concise.")
        | llm
        | StrOutputParser()
    )

    # Parallel step runs pros_chain and cons_chain concurrently!
    # RunnableParallel can be written as a dict: {"pros": pros_chain, "cons": cons_chain}
    analysis_branches = RunnableParallel(
        pros=pros_chain,
        cons=cons_chain,
        proposal=RunnablePassthrough(),  # Pass the original proposal through unchanged!
    )

    # Step 3: Synthesis prompt that takes the parallel outputs
    synthesis_prompt = ChatPromptTemplate.from_template(
        "Proposal: {proposal}\n\n"
        "Pros Identified:\n{pros}\n\n"
        "Cons Identified:\n{cons}\n\n"
        "Give a 1-sentence final executive decision on whether to proceed."
    )

    # Complete LCEL Tree:
    # 1. Branch into parallel Pros & Cons analysis
    # 2. Feed parallel outputs directly into synthesis chain
    full_decision_chain = analysis_branches | synthesis_prompt | llm | StrOutputParser()

    proposal_text = "Migrating our monolithic payment architecture to microservices in 30 days"
    print(f"Evaluating Proposal: '{proposal_text}'\n")

    decision = full_decision_chain.invoke({"proposal": proposal_text})
    print("Executive Verdict:")
    print(decision)


# =============================================================================
# MAIN RUNNER
# =============================================================================
def main():
    print("=" * 70)
    print("LANGCHAIN LESSON 2: LCEL, RUNNABLEPARALLEL & RUNNABLEPASSTHROUGH")
    print("=" * 70)

    demo_sequential_chain()
    demo_parallel_chains()


if __name__ == "__main__":
    main()

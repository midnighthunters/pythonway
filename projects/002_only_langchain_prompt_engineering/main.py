"""
===============================================================================
PROJECT 002: DYNAMIC PROMPT TEMPLATES & FEW-SHOT IN-CONTEXT LEARNING
Stage 1: Pure Fundamentals | Difficulty: 1.5 / 10 (Beginner)
===============================================================================

Core Concepts Demonstrated:
1. Dynamic ChatPromptTemplates: Multi-variable parameterization.
2. Partial Prompt Formatting: Pre-filling static application constants.
3. FewShotChatMessagePromptTemplate: Guiding model output with structured in-context examples.
4. MessagesPlaceholder: Safely inserting variable-length message history into prompts.
===============================================================================
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from config import get_llm, ACTIVE_MODEL


def demo_partial_prompt_formatting():
    """Step 1: Demonstrates pre-filling variables using .partial()."""
    print("=" * 70)
    print("STEP 1: PARTIAL PROMPT FORMATTING (prompt.partial())")
    print("=" * 70)
    print("Pre-binding constants (e.g. company name, system date) saves redundant inputs.\n")

    # Base prompt with 3 variables: company, tone, customer_issue
    base_prompt = ChatPromptTemplate.from_messages([
        ("system", "You represent {company}. Respond in a {tone} tone in 2 sentences."),
        ("human", "Customer Complaint: {customer_issue}"),
    ])

    # Pre-fill 'company' so callers only need to provide 'tone' and 'customer_issue'
    acme_support_prompt = base_prompt.partial(company="Cyberdyne Cloud Solutions")

    llm = get_llm(temperature=0.3)
    chain = acme_support_prompt | llm | StrOutputParser()

    result = chain.invoke({
        "tone": "empathetic and reassuring",
        "customer_issue": "Our production database went offline during black friday sales.",
    })

    print(f"Generated Support Response:\n{result}")
    print("-" * 70)


def demo_few_shot_prompting():
    """Step 2: Demonstrates structured Few-Shot In-Context Learning."""
    print("\n" + "=" * 70)
    print("STEP 2: FEW-SHOT IN-CONTEXT PROMPTING (FewShotChatMessagePromptTemplate)")
    print("=" * 70)
    print("Few-shot examples anchor the model to exact syntactic output patterns.\n")

    # 1. Define high-quality input/output pairs
    examples = [
        {"input": "The server latency spiked to 4500ms after the deployment.", "category": "INCIDENT_ALERT", "severity": "P1"},
        {"input": "Can we upgrade our subscription to the team plan next month?", "category": "BILLING_INQUIRY", "severity": "P3"},
        {"input": "Dark mode font contrast on the settings page is a bit low.", "category": "UI_FEEDBACK", "severity": "P4"},
    ]

    # 2. Define the template for each individual example pair
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "CATEGORY: {category} | SEVERITY: {severity}"),
    ])

    # 3. Assemble the few-shot template
    few_shot_template = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
    )

    # 4. Wrap with system instructions and the current live input
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an automated IT triage engine. Classify incoming tickets according to the examples."),
        few_shot_template,
        ("human", "{input}"),
    ])

    llm = get_llm(temperature=0.0)
    chain = final_prompt | llm | StrOutputParser()

    test_ticket = "All outbound emails from our authentication service are getting bounced as spam."
    print(f"Triage Input: '{test_ticket}'")
    result = chain.invoke({"input": test_ticket})
    print(f"Few-Shot Triage Result:\n{result}")
    print("-" * 70)


def demo_messages_placeholder():
    """Step 3: Demonstrates dynamic chat history injection via MessagesPlaceholder."""
    print("\n" + "=" * 70)
    print("STEP 3: DYNAMIC CONVERSATION HISTORY (MessagesPlaceholder)")
    print("=" * 70)
    print("Injects a list of past messages dynamically without hardcoding turn indices.\n")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an insightful coding mentor. Answer concisely."),
        MessagesPlaceholder(variable_name="chat_history"),  # Injects dynamic list of past messages!
        ("human", "{question}"),
    ])

    # Simulated past conversation turns
    history = [
        HumanMessage(content="What is a closure in Python?"),
        AIMessage(content="A closure is a nested function that retains access to variables from its enclosing scope, even after the outer function has finished executing."),
    ]

    llm = get_llm(temperature=0.2)
    chain = prompt | llm | StrOutputParser()

    # User asks a follow-up that relies on past context
    follow_up_question = "Can you give me a 3-line code example of that?"
    print(f"Follow-up Question: '{follow_up_question}' (relies on chat_history)")

    result = chain.invoke({
        "chat_history": history,
        "question": follow_up_question,
    })
    print(f"Response:\n{result}")
    print("=" * 70)


def main():
    print("*" * 70)
    print("PROJECT 002: DYNAMIC PROMPT TEMPLATES & FEW-SHOT LEARNING")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    demo_partial_prompt_formatting()
    demo_few_shot_prompting()
    demo_messages_placeholder()
    print("\n[SUCCESS] Project 002 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()

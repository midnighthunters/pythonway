"""
===============================================================================
LANGGRAPH CONCEPT 2: CONDITIONAL EDGES AND DYNAMIC ROUTING
===============================================================================

Why Conditional Edges?
---------------------
Real-world workflows aren't just straight lines. They branch dynamically based on:
  - User intent or classification results
  - Confidence thresholds
  - Tool execution success or failure
  - Sentiment analysis or business rules

In LangGraph:
  `builder.add_conditional_edges(source_node, router_function, path_map)`
  1. `source_node`: The node whose output triggers the routing decision.
  2. `router_function`: Evaluates the current state and returns a key/destination.
  3. `path_map` (optional): A dictionary mapping router output strings to node names.

In this lesson:
  1. Build an Intelligent Customer Support Triage System.
  2. Classifier node determines ticket category using Groq LLM.
  3. Router directs the state to Technical Support, Billing, or General Inquiry.
  4. Specialized handlers process the request.
  5. All paths converge at a satisfaction/follow-up node before reaching END.
===============================================================================
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from config import get_llm

# =============================================================================
# 1. DEFINE STATE
# =============================================================================
class SupportTicketState(TypedDict):
    ticket_id: str
    customer_message: str
    category: Literal["technical", "billing", "general"]  # Classified intent
    agent_response: str
    follow_up_note: str


# =============================================================================
# 2. DEFINE CLASSIFIER & ROUTER
# =============================================================================
def classifier_node(state: SupportTicketState) -> dict:
    """
    Classifier Node:
    Uses Groq LLM to inspect the customer message and classify it into
    one of three categories: 'technical', 'billing', or 'general'.
    """
    print(f"\n[CLASSIFIER] Categorizing ticket #{state['ticket_id']}...")
    llm = get_llm(temperature=0.0)

    prompt = (
        "Classify the following customer support request into EXACTLY ONE of these categories:\n"
        "- 'technical' (bugs, error codes, server issues, crashes)\n"
        "- 'billing' (invoices, refund, subscription charges, payment failures)\n"
        "- 'general' (account info, general questions, feedback)\n\n"
        f"Customer Message: '{state['customer_message']}'\n\n"
        "Reply with ONLY the single lowercase word: 'technical', 'billing', or 'general'."
    )
    response = llm.invoke(prompt)
    cleaned_category = response.content.strip().lower()

    # Validate output to guarantee clean routing
    if "technical" in cleaned_category:
        category = "technical"
    elif "billing" in cleaned_category:
        category = "billing"
    else:
        category = "general"

    print(f" -> Classification Result: [{category.upper()}]")
    return {"category": category}


def route_ticket(state: SupportTicketState) -> str:
    """
    Router Function (The Conditional Edge logic):
    Accepts current state and returns the name of the next destination node.
    Notice: This is a normal Python function, NOT a node itself.
    """
    category = state.get("category", "general")
    if category == "technical":
        return "technical_support"
    elif category == "billing":
        return "billing_support"
    else:
        return "general_support"


# =============================================================================
# 3. SPECIALIZED HANDLER NODES
# =============================================================================
def technical_support_node(state: SupportTicketState) -> dict:
    """Handles technical issues with step-by-step troubleshooting."""
    print(" -> [TECH SUPPORT NODE] Diagnosing technical issue...")
    llm = get_llm(temperature=0.2)
    prompt = (
        f"You are a Senior Technical Support Engineer. Provide a concise, technical "
        f"troubleshooting response to this issue: '{state['customer_message']}'."
    )
    res = llm.invoke(prompt)
    return {"agent_response": res.content}


def billing_support_node(state: SupportTicketState) -> dict:
    """Handles financial, payment, and refund inquiries with empathy."""
    print(" -> [BILLING SUPPORT NODE] Addressing billing query...")
    llm = get_llm(temperature=0.2)
    prompt = (
        f"You are a Billing Specialist. Provide a polite and clear answer regarding "
        f"billing policy and next steps for: '{state['customer_message']}'."
    )
    res = llm.invoke(prompt)
    return {"agent_response": res.content}


def general_support_node(state: SupportTicketState) -> dict:
    """Handles general questions and customer assistance."""
    print(" -> [GENERAL SUPPORT NODE] Handling general inquiry...")
    llm = get_llm(temperature=0.5)
    prompt = (
        f"You are a Customer Experience Representative. Answer warmly and concisely "
        f"to this inquiry: '{state['customer_message']}'."
    )
    res = llm.invoke(prompt)
    return {"agent_response": res.content}


def quality_assurance_node(state: SupportTicketState) -> dict:
    """
    Common Convergence Node:
    All branches merge back here to append standard policy & satisfaction notes.
    """
    print("\n[QA & POLICY NODE] Appending standard service disclaimer...")
    note = f"Ticket #{state['ticket_id']} handled under category [{state['category'].upper()}]."
    return {"follow_up_note": note}


# =============================================================================
# 4. ASSEMBLE GRAPH WITH CONDITIONAL EDGES
# =============================================================================
def build_support_graph():
    r"""
    Graph Flow:
                  /--> technical_support --\
      START -> classifier ---> billing_support ----> quality_assurance -> END
                  \--> general_support ---/
    """
    builder = StateGraph(SupportTicketState)

    # 1. Add all nodes
    builder.add_node("classifier", classifier_node)
    builder.add_node("technical_support", technical_support_node)
    builder.add_node("billing_support", billing_support_node)
    builder.add_node("general_support", general_support_node)
    builder.add_node("quality_assurance", quality_assurance_node)

    # 2. Add normal edge from START to classifier
    builder.add_edge(START, "classifier")

    # 3. Add CONDITIONAL EDGES from classifier using router function
    builder.add_conditional_edges(
        "classifier",  # Node after which branching occurs
        route_ticket,  # Function that inspects state and picks route
        {
            # Mapping: router output value -> node name in graph
            "technical_support": "technical_support",
            "billing_support": "billing_support",
            "general_support": "general_support",
        },
    )

    # 4. Re-converge all specialized branches into QA node
    builder.add_edge("technical_support", "quality_assurance")
    builder.add_edge("billing_support", "quality_assurance")
    builder.add_edge("general_support", "quality_assurance")

    # 5. Connect QA node to END
    builder.add_edge("quality_assurance", END)

    return builder.compile()


# =============================================================================
# 5. DEMONSTRATION WITH DIFFERENT TICKET TYPES
# =============================================================================
def main():
    print("=" * 70)
    print("LANGGRAPH LESSON 2: CONDITIONAL EDGES & DYNAMIC ROUTING")
    print("=" * 70)

    graph = build_support_graph()

    test_tickets = [
        {
            "ticket_id": "TCK-101",
            "customer_message": "Our database connection times out with error code 504 on the production API gateway.",
        },
        {
            "ticket_id": "TCK-102",
            "customer_message": "I was charged $49 twice on my Mastercard for this month's Pro subscription. Please issue a refund.",
        },
        {
            "ticket_id": "TCK-103",
            "customer_message": "Can you tell me what hours your live chat support is open and where to find documentation?",
        },
    ]

    for ticket in test_tickets:
        print("\n" + "=" * 60)
        print(f"PROCESSING TICKET {ticket['ticket_id']}: '{ticket['customer_message']}'")
        print("=" * 60)

        initial_state = {
            "ticket_id": ticket["ticket_id"],
            "customer_message": ticket["customer_message"],
            "category": "general",
            "agent_response": "",
            "follow_up_note": "",
        }

        result = graph.invoke(initial_state)

        print("\n--- FINAL RESOLUTION ---")
        print(f"Assigned Category: {result['category'].upper()}")
        print(f"Agent Response:\n{result['agent_response']}")
        print(f"Follow-up Note: {result['follow_up_note']}")

        png_bytes = graph.get_graph().draw_mermaid_png()

        with open("support_graph.png", "wb") as f:
            f.write(png_bytes)


if __name__ == "__main__":
    main()

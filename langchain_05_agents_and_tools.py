"""
===============================================================================
LANGCHAIN CONCEPT 5: AGENTS, TOOLS, AND THE EVOLUTION TO LANGGRAPH
===============================================================================

What is an Agent in LangChain?
------------------------------
In a standard chain, the sequence of steps is hardcoded:
  Input -> Step 1 -> Step 2 -> Output.

In an Agent, an LLM acts as a reasoning engine to decide:
  1. Which tool to call (if any)
  2. What arguments to pass to the tool
  3. When enough information is gathered to provide the final answer

Evolution of Agents (From AgentExecutor to LangGraph):
-----------------------------------------------------
1. Classic LangChain: `AgentExecutor`
   - A Python `while` loop that managed tool execution.
   - Limitation: Hard to inspect internal state, difficult to add human-in-the-loop
     approval gates, and awkward for complex multi-agent handoffs.
2. Modern LangChain: `create_agent` (Powered by LangGraph under the hood!)
   - Compiles directly into a LangGraph graph.
   - Provides full state inspection, checkpoint persistence, and modular nodes.

In this lesson:
  1. Define custom tools using the `@tool` decorator.
  2. Build a modern Agent with `create_agent`.
  3. Execute multi-step research queries requiring multiple tools.
  4. Compare LangChain Agents vs LangGraph workflows.
===============================================================================
"""

from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config import get_llm


# =============================================================================
# 1. DEFINE TOOLS
# =============================================================================
@tool
def get_weather(city: str) -> str:
    """
    Returns current weather, temperature in Celsius, and atmospheric condition
    for a given city (e.g. 'Tokyo', 'London', 'San Francisco').
    """
    print(f"\n   [TOOL EXECUTING] get_weather('{city}')")
    database = {
        "tokyo": "19°C, Partly Cloudy, Humidity 62%",
        "london": "14°C, Light Drizzle, Humidity 85%",
        "san francisco": "17°C, Sunny, Humidity 55%",
        "new york": "22°C, Clear Skies, Humidity 48%",
    }
    key = city.strip().lower()
    return database.get(key, f"Weather data for '{city}' is currently unavailable.")


@tool
def search_flight_availability(origin: str, destination: str) -> str:
    """
    Searches available direct and connecting flights between two cities.
    """
    print(f"\n   [TOOL EXECUTING] search_flight_availability('{origin}', '{destination}')")
    return (
        f"Available Flights ({origin.upper()} -> {destination.upper()}):\n"
        f"1. Flight PA-104 | Departs: 08:30 AM | Arrives: 04:45 PM | Price: $680 (Direct)\n"
        f"2. Flight PA-219 | Departs: 02:15 PM | Arrives: 10:30 PM | Price: $540 (1 stop)"
    )


tools_list = [get_weather, search_flight_availability]


# =============================================================================
# 2. MODERN LANGCHAIN AGENT (create_agent)
# =============================================================================
def demo_modern_agent():
    print("=" * 70)
    print("PART 1: MODERN AGENT (create_agent)")
    print("=" * 70)
    print("The modern agent uses Groq tool-calling to resolve complex queries.\n")

    llm = get_llm(temperature=0.0)

    # create_agent compiles directly into a LangGraph graph under the hood!
    agent = create_agent(
        model=llm,
        tools=tools_list,
        system_prompt="You are a professional travel coordinator. Always use tools to verify facts.",
    )

    query = (
        "I am planning a trip. Can you check the current weather in Tokyo, "
        "and also find flights from San Francisco to Tokyo?"
    )

    print(f"User Request: '{query}'\n")
    print("Agent is reasoning and executing tools...")

    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    final_message = response["messages"][-1]
    print("\n" + "=" * 60)
    print("FINAL SYNTHESIZED AGENT RESPONSE:")
    print("=" * 60)
    print(final_message.content)


# =============================================================================
# 3. CLASSIC AGENT (AgentExecutor)
# =============================================================================
def demo_classic_agent_executor():
    print("\n" + "=" * 70)
    print("PART 2: CLASSIC AGENT (create_tool_calling_agent + AgentExecutor)")
    print("=" * 70)
    print("How LangChain traditionally built agents prior to LangGraph:\n")

    llm = get_llm(temperature=0.0)

    # Prompt with agent_scratchpad placeholder for tool history
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant with access to weather tools."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent_runnable = create_tool_calling_agent(llm, [get_weather], prompt)
    executor = AgentExecutor(agent=agent_runnable, tools=[get_weather], verbose=False)

    res = executor.invoke({"input": "What's the weather like in London right now?"})
    print(f"Executor Output: {res['output']}\n")


# =============================================================================
# 4. ARCHITECTURAL COMPARISON: LANGCHAIN VS LANGGRAPH
# =============================================================================
def print_comparison():
    print("=" * 70)
    print("LANGCHAIN vs LANGGRAPH: WHEN TO USE WHICH?")
    print("=" * 70)
    comparison = """
+-----------------------+-----------------------------+-----------------------------+
| Feature               | LangChain (Chains & LCEL)   | LangGraph (Stateful Graphs) |
+-----------------------+-----------------------------+-----------------------------+
| Core Paradigm         | Directed Acyclic (Linear)   | Directed Graphs with LOOPS  |
| Flow Control          | Pipe operator: A | B | C    | Nodes, Edges, Routers       |
| Best Use Case         | RAG, Prompts, Extraction    | Autonomous Multi-Agent Apps |
| State Management      | Transient (passes through)  | First-class Typed State     |
| Memory / Checkpoints  | Manual buffer / storage     | Native MemorySaver / DBs    |
| Human-in-the-Loop     | Difficult (custom pauses)   | Built-in (interrupt_before) |
| Architecture          | Simple Pipelines            | Complex Systems & Workflows |
+-----------------------+-----------------------------+-----------------------------+
"""
    print(comparison)


# =============================================================================
# MAIN RUNNER
# =============================================================================
def main():
    print("=" * 70)
    print("LANGCHAIN LESSON 5: TOOLS, AGENTS & ARCHITECTURE COMPARISON")
    print("=" * 70)

    demo_modern_agent()
    demo_classic_agent_executor()
    print_comparison()


if __name__ == "__main__":
    main()

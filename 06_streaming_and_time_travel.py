"""
===============================================================================
LANGGRAPH CONCEPT 6: STREAMING MODES AND TIME TRAVEL (STATE REPLAY)
===============================================================================

Why Streaming & Time Travel?
---------------------------
1. STREAMING:
   In chat applications or interactive UIs, waiting for a long multi-agent workflow
   to finish completely leads to poor user experience. LangGraph provides multiple
   streaming modes:
     - `stream_mode="updates"`: Yields state changes node-by-node in real time.
     - `stream_mode="values"`: Yields full state after each step.
     - `stream_mode="messages"`: Yields tokens chunk-by-chunk directly from the LLM.

2. TIME TRAVEL:
   Because every step is captured by the checkpointer, LangGraph allows:
     - Auditing: Reviewing exact past state snapshots.
     - Rewinding: Going back to a past checkpoint.
     - Forking: Modifying a past state and running forward from that point
       to explore "What if?" branches or recover from errors.

In this lesson:
  1. Stream node updates live as they execute.
  2. Stream tokens in real time from Groq LLM.
  3. Inspect checkpoint history and demonstrate Time Travel rewinding.
===============================================================================
"""

from typing import TypedDict
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from config import get_llm


# =============================================================================
# 1. NODE UPDATES STREAMING DEMO
# =============================================================================
class PipelineState(TypedDict):
    query: str
    fact_1: str
    fact_2: str
    summary: str


def node_alpha(state: PipelineState) -> dict:
    llm = get_llm(temperature=0.0)
    res = llm.invoke(f"State one interesting fact about space exploration in 15 words: '{state['query']}'")
    return {"fact_1": res.content.strip()}


def node_beta(state: PipelineState) -> dict:
    llm = get_llm(temperature=0.0)
    res = llm.invoke(f"State one surprising fact about the solar system in 15 words: '{state['query']}'")
    return {"fact_2": res.content.strip()}


def node_gamma(state: PipelineState) -> dict:
    llm = get_llm(temperature=0.0)
    res = llm.invoke(
        f"Combine these two facts into a cohesive 1-sentence summary:\n"
        f"1. {state['fact_1']}\n2. {state['fact_2']}"
    )
    return {"summary": res.content.strip()}


def build_streaming_pipeline():
    builder = StateGraph(PipelineState)
    builder.add_node("alpha", node_alpha)
    builder.add_node("beta", node_beta)
    builder.add_node("gamma", node_gamma)

    builder.add_edge(START, "alpha")
    builder.add_edge("alpha", "beta")
    builder.add_edge("beta", "gamma")
    builder.add_edge("gamma", END)

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


# =============================================================================
# 2. RUN DEMONSTRATIONS
# =============================================================================
def demo_node_streaming(graph):
    print("=" * 70)
    print("PART 1: STREAMING NODE-LEVEL UPDATES (stream_mode='updates')")
    print("=" * 70)
    print("Instead of waiting for all 3 nodes to finish, observe updates as each node yields:")

    config = {"configurable": {"thread_id": "stream-demo-1"}}
    inputs = {
        "query": "Voyager probes",
        "fact_1": "",
        "fact_2": "",
        "summary": "",
    }

    # stream_mode='updates' emits a dict: {node_name: {updated_fields}}
    for update in graph.stream(inputs, config=config, stream_mode="updates"):
        for node_name, state_patch in update.items():
            print(f"\n[STREAMED UPDATE FROM NODE: '{node_name}']")
            for k, v in state_patch.items():
                print(f"   {k} => {v}")


def demo_token_streaming():
    print("\n" + "=" * 70)
    print("PART 2: REAL-TIME TOKEN STREAMING (stream_mode='messages')")
    print("=" * 70)
    print("Streaming tokens live as Groq generates them:\n")

    builder = StateGraph(MessagesState)
    llm = get_llm(temperature=0.7)
    builder.add_node("llm_node", lambda s: {"messages": [llm.invoke(s["messages"])]})
    builder.add_edge(START, "llm_node")
    builder.add_edge("llm_node", END)
    chat_graph = builder.compile()

    prompt = [HumanMessage(content="Write a haiku about compiling code in the dark.")]

    print("Agent: ", end="", flush=True)
    # stream_mode='messages' yields individual token chunks as they arrive from Groq
    for msg_chunk, metadata in chat_graph.stream({"messages": prompt}, stream_mode="messages"):
        if msg_chunk.content:
            print(msg_chunk.content, end="", flush=True)
    print("\n")


def demo_time_travel(graph):
    print("=" * 70)
    print("PART 3: TIME TRAVEL & CHECKPOINT INSPECTION")
    print("=" * 70)

    config = {"configurable": {"thread_id": "stream-demo-1"}}

    # Fetch chronological history of all checkpoints saved for this thread
    print("\nRetrieving checkpoint snapshots from MemorySaver...")
    history = list(graph.get_state_history(config))

    print(f"Total recorded states for thread: {len(history)}\n")
    for i, snapshot in enumerate(history):
        step_id = snapshot.config["configurable"]["checkpoint_id"]
        step_name = snapshot.metadata.get("step", "init")
        node_next = snapshot.next
        print(f"[{i}] Checkpoint: {step_id[:8]}... | Step: {step_name} | Next: {node_next}")
        if snapshot.values.get("summary"):
            print(f"    Summary in this state: {snapshot.values['summary'][:60]}...")

    # Demonstrating Rewind:
    # Let's rewind to an earlier checkpoint before gamma (the summary node) ran
    # history[0] is latest (END), history[1] is after beta, before gamma
    if len(history) >= 2:
        earlier_checkpoint = history[1]
        print(f"\n[TIME TRAVEL ACTION]: Rewinding back to checkpoint before 'gamma' ran...")
        print(f"Rewind Target Next Node: {earlier_checkpoint.next}")

        # Fork state by injecting a modified fact
        print("Injecting an edited fact into the past state...")
        graph.update_state(
            earlier_checkpoint.config,
            {"fact_2": "Jupiter has a massive storm known as the Great Red Spot."},
        )

        print("Resuming execution from the rewound point...")
        new_result = graph.invoke(None, config=earlier_checkpoint.config)

        print("\n--- NEW REPLAYED SUMMARY FROM TIME TRAVEL BRANCH ---")
        print(new_result.get("summary"))


def main():
    print("=" * 70)
    print("LANGGRAPH LESSON 6: STREAMING & TIME TRAVEL")
    print("=" * 70)

    pipeline = build_streaming_pipeline()
    demo_node_streaming(pipeline)
    demo_token_streaming()
    demo_time_travel(pipeline)


if __name__ == "__main__":
    main()

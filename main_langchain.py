"""
===============================================================================
LANGCHAIN MASTER SHOWCASE & INTERACTIVE APPLICATION
===============================================================================

This is the main entry point for the LangChain Groq project.
You can:
  [1] Run Lesson 1: Models, Messages, Prompt Templates & Streaming
  [2] Run Lesson 2: LCEL Chains (Pipe Operator, Parallel, Passthrough)
  [3] Run Lesson 3: Structured Outputs & Schema Enforcement (Pydantic)
  [4] Run Lesson 4: Retrieval-Augmented Generation (RAG Pipeline)
  [5] Run Lesson 5: Agents, Tools & LangChain vs LangGraph Comparison
  [6] Run Full LangChain Test Suite (Verifies all 5 lessons end-to-end)
  [7] Launch Interactive LCEL Playground
  [0] Exit
===============================================================================
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows command line
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import ACTIVE_MODEL, get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def launch_interactive_playground():
    """Interactive LCEL chain playground in terminal."""
    print("\n" + "=" * 70)
    print("LIVE INTERACTIVE LCEL PLAYGROUND (LangChain + Groq)")
    print(f"Model: {ACTIVE_MODEL}")
    print("Type your question or prompt, and watch the LCEL chain stream the answer!")
    print("Type 'exit' or 'quit' to return to menu.")
    print("=" * 70)

    llm = get_llm(temperature=0.4)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an articulate AI expert assistant. Answer clearly and concisely."),
        ("human", "{user_input}"),
    ])
    chain = prompt | llm | StrOutputParser()

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Returning to main menu...")
                break

            print("\nAI: ", end="", flush=True)
            for chunk in chain.stream({"user_input": user_input}):
                print(chunk, end="", flush=True)
            print()

        except (KeyboardInterrupt, EOFError):
            print("\nExiting playground...")
            break
        except Exception as e:
            print(f"\nError: {e}")


def run_all_langchain_tests():
    """Runs all 5 LangChain lessons in sequence."""
    print("\n" + "=" * 70)
    print("RUNNING COMPLETE LANGCHAIN VERIFICATION SUITE")
    print("=" * 70)

    lessons = [
        ("Lesson 1: Models & Prompts", "langchain_01_prompts_and_models.py"),
        ("Lesson 2: LCEL & Chains", "langchain_02_lcel_chains.py"),
        ("Lesson 3: Structured Outputs", "langchain_03_structured_output.py"),
        ("Lesson 4: RAG Pipeline", "langchain_04_rag_pipeline.py"),
        ("Lesson 5: Agents & Tools", "langchain_05_agents_and_tools.py"),
    ]

    for title, script in lessons:
        print(f"\n>>> Running {title} ({script})...")
        ret = os.system(f'"{sys.executable}" {script}')
        if ret != 0:
            print(f"❌ {title} FAILED with exit code {ret}")
            return False
        else:
            print(f"✅ {title} PASSED!")

    print("\n" + "=" * 70)
    print("🎉 ALL 5 LANGCHAIN LESSONS PASSED SUCCESSFULLY!")
    print("=" * 70)
    return True


def display_menu():
    print("\n" + "=" * 70)
    print("          LANGCHAIN COMPREHENSIVE LEARNING SUITE")
    print(f"   Provider: Groq | Active Model: {ACTIVE_MODEL}")
    print("=" * 70)
    print(" [1] Lesson 1: Models, Messages, Prompt Templates & Streaming")
    print(" [2] Lesson 2: LCEL Chains (Pipe Operator, Parallel, Passthrough)")
    print(" [3] Lesson 3: Structured Outputs & Schema Enforcement (Pydantic)")
    print(" [4] Lesson 4: Retrieval-Augmented Generation (RAG Pipeline)")
    print(" [5] Lesson 5: Agents, Tools & LangChain vs LangGraph Comparison")
    print(" [6] Run All Lessons (Verification Test Suite)")
    print(" [7] Launch Interactive LCEL Playground")
    print(" [0] Exit")
    print("=" * 70)


def main():
    while True:
        display_menu()
        choice = input("Enter option (0-7): ").strip()

        if choice == "1":
            import importlib
            mod = importlib.import_module("langchain_01_prompts_and_models")
            mod.main()
        elif choice == "2":
            import importlib
            mod = importlib.import_module("langchain_02_lcel_chains")
            mod.main()
        elif choice == "3":
            import importlib
            mod = importlib.import_module("langchain_03_structured_output")
            mod.main()
        elif choice == "4":
            import importlib
            mod = importlib.import_module("langchain_04_rag_pipeline")
            mod.main()
        elif choice == "5":
            import importlib
            mod = importlib.import_module("langchain_05_agents_and_tools")
            mod.main()
        elif choice == "6":
            run_all_langchain_tests()
        elif choice == "7":
            launch_interactive_playground()
        elif choice in ("0", "exit", "quit", "q"):
            print("Exiting. Happy LangChain hacking!")
            break
        else:
            print("Invalid choice, please select between 0 and 7.")


if __name__ == "__main__":
    main()

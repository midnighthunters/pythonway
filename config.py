"""
Configuration Module for LangGraph Groq Project.

Handles:
- Loading environment variables from .env
- Setting UTF-8 console output for Windows terminals
- Initializing ChatGroq with automatic model validation and fallback
"""

import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq

# Ensure UTF-8 output encoding for Windows command line (prevents UnicodeEncodeError)
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Load environment variables from .env file
load_dotenv()

# Read Groq API Key and Preferred Model
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Please add your Groq API key to the .env file."
    )

# Fallback models in priority order if preferred model is not accessible
FALLBACK_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama3-70b-8192",
    "llama3-8b-8192",
]


def resolve_model_name() -> str:
    """
    Checks if the requested model is accessible on Groq for this API key.
    If not, automatically falls back to an available chat model.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        available_models = [m.id for m in client.models.list().data]

        if DEFAULT_MODEL in available_models:
            return DEFAULT_MODEL

        # Look for fallback
        for fb in FALLBACK_MODELS:
            if fb in available_models:
                print(f"[INFO] Configured model '{DEFAULT_MODEL}' is not available on this API key.")
                print(f"[INFO] Automatically falling back to active chat model: '{fb}'.\n")
                return fb

        # If none matched, return whatever the user specified
        return DEFAULT_MODEL
    except Exception:
        # If API listing fails, return user configured model
        return DEFAULT_MODEL


ACTIVE_MODEL = resolve_model_name()


def get_llm(temperature: float = 0.0) -> ChatGroq:
    """
    Returns an instantiated ChatGroq model instance ready for LangGraph nodes.
    """
    return ChatGroq(
        model=ACTIVE_MODEL,
        api_key=GROQ_API_KEY,
        temperature=temperature,
    )


if __name__ == "__main__":
    print(f"Loaded Groq Configuration:")
    print(f" - Active Model: {ACTIVE_MODEL}")
    llm = get_llm()
    test_res = llm.invoke("Hello, Groq! Confirm you are working in 10 words or less.")
    print(f" - Test Response: {test_res.content}")

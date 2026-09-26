"""
Configuration for Project 029: Contract Net Protocol (CNP).
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

root_dir = Path(__file__).resolve().parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please check the root .env file.")

from langchain_groq import ChatGroq
from groq import Groq

FALLBACK_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
]


def resolve_model() -> str:
    try:
        client = Groq(api_key=GROQ_API_KEY)
        models = [m.id for m in client.models.list().data]
        if DEFAULT_MODEL in models:
            return DEFAULT_MODEL
        for fb in FALLBACK_MODELS:
            if fb in models:
                return fb
        return DEFAULT_MODEL
    except Exception:
        return DEFAULT_MODEL


ACTIVE_MODEL = resolve_model()


def get_llm(temperature: float = 0.0) -> ChatGroq:
    return ChatGroq(
        model=ACTIVE_MODEL,
        api_key=GROQ_API_KEY,
        temperature=temperature,
    )

# Project 001: Hello LCEL: Chat Models, Messages & Unix Pipes

> **Stage**: Stage 1: Pure Fundamentals  
> **Difficulty**: 1.0 / 10 (Beginner)  
> **Primary Pillars**: `LangChain`  
> **Auxiliary Disciplines**: `LangSmith Tracing`  

---

## 🎯 Learning Objective
Master `ChatGroq`, message abstractions (`SystemMessage`, `HumanMessage`, `AIMessage`), the declarative LangChain Expression Language (LCEL) pipe syntax (`|`), and attaching LangSmith run telemetry.

---

## 🧠 Key Concepts Covered
- **ChatGroq**: Instantiating and configuring high-throughput inference models.
- **Message Roles**: Distinguishing between developer system instructions, human prompts, and assistant memory.
- **LCEL Pipe (`|`)**: Declarative chaining of `Runnable` objects without imperative boilerplate.
- **`StrOutputParser`**: Unpacking `AIMessage` objects directly into pure Python strings.
- **Streaming & Batching**: Real-time token delivery via `.stream()` and concurrent evaluation via `.batch()`.
- **LangSmith Telemetry**: Attaching `tags` and `metadata` to trace runs in observability platforms.

---

## 🏗️ Architecture & Control Flow
```text
User Input Dict
      │
      ▼
┌─────────────────────────┐
│   ChatPromptTemplate    │  formats {language} and {text} into System/Human messages
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│     ChatGroq (LLM)      │  executes inference via Groq high-speed engine
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│     StrOutputParser     │  extracts AIMessage.content into clean string
└───────────┬─────────────┘
            │
            ▼
    Final Output String (Traced in LangSmith)
```

---

## 📂 Project Structure
```text
001_only_langchain_hello_lcel/
├── README.md              # Project specifications, self-quiz & stretch challenge
├── requirements.txt       # Dependencies for this project
├── config.py              # Groq model and environment configuration
├── main.py                # Pedagogical runnable demonstration
└── test_verification.py   # Automated assertion tests
```

---

## 🚀 Execution & Verification Guide

### 1. Run Main Demonstration
```bash
python main.py
```

### 2. Run Automated Verification Tests
```bash
python test_verification.py
```

---

## 📝 Self-Assessment Interview Quiz (Test Your Understanding)

1. **Why does LangChain use structured message objects (`SystemMessage`, `HumanMessage`, `AIMessage`) instead of a single raw string prompt?**
   * *Answer*: Modern chat models (like Llama 3, GPT-4) are trained on structured multi-turn conversation formats with explicit role demarcations. Passing typed objects preserves role boundaries, avoids prompt injection between system instructions and untrusted user input, and mirrors the model's native API.

2. **What interface must a Python class implement to be compatible with the LCEL pipe operator (`|`)?**
   * *Answer*: It must implement the `Runnable` protocol, which requires `.invoke()`, `.stream()`, `.batch()`, and their asynchronous equivalents (`.ainvoke()`, `.astream()`, `.abatch()`).

3. **How does `StrOutputParser()` differ from accessing `response.content` manually?**
   * *Answer*: `StrOutputParser` is a composable `Runnable`. In a streaming LCEL chain (`prompt | model | StrOutputParser()`), it seamlessly passes token chunks as strings to downstream consumers without breaking the stream, whereas manual property access requires waiting for the complete response object.

---

## 🏆 Stretch Challenge
**Task**: Modify `main.py` to create a chain that takes an English sentence, translates it into French and German **simultaneously in a single batch call**, and prints the token latency for each translation.
*(Hint: Use `chain.batch([{"language": "French", "text": ...}, {"language": "German", "text": ...}])`).*

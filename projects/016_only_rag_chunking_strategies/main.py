"""
===============================================================================
PROJECT 016: DOCUMENT INGESTION & CHUNKING STRATEGY BENCHMARK
Stage 1: Pure Fundamentals | Difficulty: 2.0 / 10 (Beginner Friendly)
===============================================================================

THE BIG QUESTION:
Why do we need "Chunking" in RAG (Retrieval-Augmented Generation)?

Suppose you have a 50-page employee manual, medical guide, or legal code.
You CANNOT just throw the whole 50 pages into an embedding model at once because:
1. Embedding models have token limits (e.g. 512, 1024 tokens).
2. If you embed 50 pages into a single vector, it becomes a blurry "average" of
   everything, making specific needle-in-a-haystack retrieval impossible.
3. Sending 50 pages on every query wastes money, increases latency, and degrades
   LLM attention.

SOLUTION:
We slice the document into bite-sized pieces called "CHUNKS".
But HOW you slice them makes the difference between a smart AI and a broken AI!

In this project, we explore 3 core chunking strategies on a fun, relatable document:
  "The Cozy Coffee & Bakery Employee Handbook"

Strategies Explored:
1. Naive Fixed-Character Slicing (The Flawed Way - slices words in half!)
2. Recursive Character Splitting (The Industry Gold Standard - respects paragraphs & words)
3. Structural Markdown Splitting (Extracts headers into rich search metadata)
4. The Power of Chunk Overlap (Building semantic bridges across cuts)
5. Live Mini-RAG generation with Groq LLM!
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import re
from typing import List, Dict, Any
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)
from langchain_core.documents import Document
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. OUR SAMPLE RELATABLE DOCUMENT: THE COFFEE SHOP HANDBOOK
# =============================================================================
SAMPLE_HANDBOOK_MARKDOWN = """# Cozy Coffee & Bakery Handbook

## 1. Operating Hours & Breaks
Welcome to the team! Our cafe doors open daily at 6:30 AM and close at 8:00 PM.
Full-time baristas receive a 45-minute paid lunch break and two 15-minute coffee tastings.
Please always clock in using your digital fingerprint scanner at the front counter.

## 2. Kitchen Safety & Microwave Rules
Kitchen cleanliness is our highest operational priority.
All cutting boards must be sanitized immediately after preparing dairy or gluten pastries.
CRITICAL RULE: Never heat seafood or pungent fish in the employee breakroom microwave!
Anyone who violates this rule will be designated as the official refrigerator cleaner for the week.

## 3. Wi-Fi & POS Cash Register
The staff private network SSID is 'CozyStaff_5G'.
The secret Wi-Fi password is 'MochaLatte#2026!'.
Never share this network with customers; customers must connect to 'CozyGuest_Free'.
If the POS cash register freezes, hold down the green reset button for 5 seconds to reboot.

## 4. Emergency Evacuation
In the event of a kitchen fire, the primary emergency exit is through the pantry backdoor.
The fire extinguisher is mounted directly beside the espresso bean grinder.
The outdoor meeting assembly point is across the street beside the blue fountain.
"""


# =============================================================================
# STRATEGY 1: NAIVE FIXED-CHARACTER CHUNKING (The Flawed Way)
# =============================================================================
def naive_fixed_chunking(text: str, chunk_size: int = 140) -> List[str]:
    """
    Slices text blindly every N characters like a blunt pizza cutter.
    Watch what happens to words at the borders!
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


# =============================================================================
# STRATEGY 2: RECURSIVE CHARACTER TEXT SPLITTING (The Gold Standard)
# =============================================================================
def recursive_chunking(
    text: str,
    chunk_size: int = 180,
    chunk_overlap: int = 40,
) -> List[Document]:
    """
    RecursiveCharacterTextSplitter:
    Tries separators in hierarchical order:
      1. "\n\n" (Double newlines = Paragraphs)
      2. "\n"   (Single newlines = Sentences/lines)
      3. " "    (Spaces = Words)
      4. ""     (Characters = absolute last resort)

    Result: Words and paragraphs stay intact whenever possible!
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )
    docs = splitter.create_documents([text])
    return docs


# =============================================================================
# STRATEGY 3: STRUCTURAL MARKDOWN HEADER CHUNKING (Metadata-Aware)
# =============================================================================
def markdown_header_chunking(markdown_text: str) -> List[Document]:
    """
    MarkdownHeaderTextSplitter:
    Slices text based on document headers (# Header 1, ## Header 2).
    Crucially, it attaches the header names as METADATA to each chunk!
    """
    headers_to_split_on = [
        ("#", "Document Title"),
        ("##", "Section Title"),
    ]
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,
    )
    return splitter.split_text(markdown_text)


# =============================================================================
# HELPER: DETECT BROKEN WORDS (To measure chunking quality)
# =============================================================================
def count_broken_words(chunks: List[str]) -> int:
    """
    Checks if a chunk starts or ends in the middle of an alphanumeric word.
    A naive slice produces broken tokens like 'micr' or 'owave'.
    """
    broken = 0
    for chunk in chunks:
        clean = chunk.strip()
        if not clean:
            continue
        # If the chunk starts mid-word (previous char was letter, first char is letter without boundary)
        # We check if first char is lowercase and not preceded by space in original text
        if re.match(r"^[a-z]", clean):
            broken += 1
    return broken


# =============================================================================
# MAIN DEMONSTRATION & BENCHMARK
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 016: DOCUMENT INGESTION & CHUNKING STRATEGY BENCHMARK")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    print("\n[DOCUMENT PREVIEW]:")
    print(f"Total Document Length: {len(SAMPLE_HANDBOOK_MARKDOWN)} characters")
    print(f"Document Sections: 4 sections (Hours, Kitchen Rules, Wi-Fi, Emergency)\n")

    # -------------------------------------------------------------------------
    # PART 1: NAIVE CHUNKING DEMO (SEE THE PROBLEM)
    # -------------------------------------------------------------------------
    print("-" * 75)
    print("STRATEGY 1: Naive Fixed-Character Chunking (chunk_size=140, overlap=0)")
    print("-" * 75)
    naive_chunks = naive_fixed_chunking(SAMPLE_HANDBOOK_MARKDOWN, chunk_size=140)

    print(f"Generated {len(naive_chunks)} naive chunks. Let's inspect Chunks 3 & 4:")
    for idx in [2, 3]:
        print(f"\n--- [Naive Chunk {idx + 1}] ---")
        print(repr(naive_chunks[idx]))

    print("\n>>> NOTICE THE PROBLEM:")
    print("Look at the boundary between chunks! Words get cut right in half!")
    print("If a user searches for 'microwave', the vector search might fail because")
    print("the word was split into two pieces across separate chunks!")

    # -------------------------------------------------------------------------
    # PART 2: RECURSIVE CHUNKING DEMO (THE GOLD STANDARD)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("STRATEGY 2: Recursive Character Chunking (chunk_size=200, overlap=40)")
    print("-" * 75)
    rec_docs = recursive_chunking(SAMPLE_HANDBOOK_MARKDOWN, chunk_size=200, chunk_overlap=40)

    print(f"Generated {len(rec_docs)} recursive chunks. Let's inspect Chunk 2 & 3:")
    for i, doc in enumerate(rec_docs[1:3], start=2):
        print(f"\n--- [Recursive Chunk {i}] (Length: {len(doc.page_content)} chars) ---")
        print(doc.page_content)

    print("\n>>> NOTICE THE DIFFERENCE:")
    print("1. Words are NEVER cut in half! (Clean word boundaries).")
    print("2. Paragraphs stay intact when they fit inside the chunk_size.")
    print("3. Notice the 40-character OVERLAP: the end of Chunk 2 shares context")
    print("   with the beginning of Chunk 3, creating a semantic bridge!")

    # -------------------------------------------------------------------------
    # PART 3: STRUCTURAL MARKDOWN HEADER CHUNKING (METADATA-AWARE)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("STRATEGY 3: Markdown Header Chunking (Splits on # and ##)")
    print("-" * 75)
    md_docs = markdown_header_chunking(SAMPLE_HANDBOOK_MARKDOWN)

    print(f"Generated {len(md_docs)} structured chunks. Each section is a clean chunk:")
    for i, doc in enumerate(md_docs, 1):
        print(f"\n--- [Markdown Section Chunk {i}] ---")
        print(f"Metadata Tag : {doc.metadata}")
        preview = doc.page_content.strip().split("\n")[0]
        print(f"Content Line 1: {preview}")

    print("\n>>> NOTICE THE POWER OF METADATA:")
    print("Each chunk automatically inherits its parent header tags!")
    print("In production RAG, you can filter by section: {'Section Title': 'Kitchen Safety'}")
    print("before performing semantic search!")

    # -------------------------------------------------------------------------
    # PART 4: COMPARATIVE BENCHMARK TABLE
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("CHUNKING STRATEGY BENCHMARK SUMMARY")
    print("=" * 75)
    print(f"{'Strategy':<30} | {'Chunks':<8} | {'Avg Chars':<10} | {'Metadata Preserved':<18}")
    print("-" * 75)

    avg_naive = sum(len(c) for c in naive_chunks) / len(naive_chunks)
    avg_rec = sum(len(d.page_content) for d in rec_docs) / len(rec_docs)
    avg_md = sum(len(d.page_content) for d in md_docs) / len(md_docs)

    print(f"{'1. Naive Fixed-Character':<30} | {len(naive_chunks):<8} | {avg_naive:<10.1f} | {'No (0 keys)':<18}")
    print(f"{'2. Recursive Character':<30} | {len(rec_docs):<8} | {avg_rec:<10.1f} | {'No (raw text)':<18}")
    print(f"{'3. Markdown Header Split':<30} | {len(md_docs):<8} | {avg_md:<10.1f} | {'YES (Header tags)':<18}")
    print("=" * 75)

    # -------------------------------------------------------------------------
    # PART 5: LIVE MINI-RAG DEMONSTRATION WITH GROQ LLM
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("LIVE MINI-RAG DEMONSTRATION")
    print("Query: 'Can I reheat my salmon fish pasta in the breakroom microwave?'")
    print("=" * 75)

    # 1. Simulate Retrieval: find the chunk mentioning 'microwave'
    retrieved_chunk = None
    for doc in md_docs:
        if "microwave" in doc.page_content.lower():
            retrieved_chunk = doc
            break

    print(f"Retrieved Relevant Chunk from Section: {retrieved_chunk.metadata.get('Section Title')}")
    print(f"Context Provided to LLM:\n\"\"\"\n{retrieved_chunk.page_content.strip()}\n\"\"\"")

    # 2. Ask Groq LLM using ONLY the retrieved chunk
    llm = get_llm(temperature=0.0)
    prompt = (
        "You are an employee compliance assistant. Answer the user's question based ONLY "
        "on the provided handbook excerpt.\n\n"
        f"Handbook Excerpt:\n{retrieved_chunk.page_content}\n\n"
        "User Question: Can I reheat my salmon fish pasta in the breakroom microwave?\n"
        "State clearly whether it is allowed and what penalty applies if violated."
    )

    print("\n[Groq LLM Response]:")
    response = llm.invoke(prompt)
    print(response.content.strip())

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 016 demonstration completed cleanly!")


if __name__ == "__main__":
    main()

"""
===============================================================================
LANGCHAIN CONCEPT 4: RETRIEVAL-AUGMENTED GENERATION (RAG) WITH LCEL
===============================================================================

What is RAG?
------------
Large Language Models have static knowledge frozen at training time, and know
nothing about your internal documentation, company policies, or live databases.
RAG solves this by:
  1. Chunking: Splitting large documents into smaller text passages.
  2. Embedding & Indexing: Storing text chunks in a Vector Store.
  3. Retrieval: Finding the top most relevant passages for a user query.
  4. Augmented Generation: Feeding the retrieved passages into the LLM prompt
     so the model answers with grounded facts and zero hallucinations!

Key LangChain components covered:
  - `Document`: The core data abstraction for text chunks + metadata.
  - `RecursiveCharacterTextSplitter`: Splits text while keeping paragraphs intact.
  - `InMemoryVectorStore`: Fast, local vector database for fast similarity search.
  - The Classic RAG LCEL Chain:
      {"context": retriever | format_docs, "question": RunnablePassthrough()}
      | prompt | llm | StrOutputParser()
===============================================================================
"""

import re
import numpy as np
from typing import List
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import get_llm


# =============================================================================
# 1. LIGHTWEIGHT, ZERO-DEPENDENCY VECTOR EMBEDDINGS
# =============================================================================
class LocalKeywordEmbeddings(Embeddings):
    """
    Fast, dependency-free bag-of-words / n-gram embedding generator.
    Allows complete, offline vector similarity search without needing
    external embedding API keys or heavy PyTorch libraries.
    """
    def __init__(self, dimensions: int = 1024):
        self.dimensions = dimensions

    def _embed(self, text: str) -> List[float]:
        vector = np.zeros(self.dimensions, dtype=float)
        words = re.findall(r"\w+", text.lower())
        for word in words:
            # Hash word into fixed-dimension vector bucket
            idx = abs(hash(word)) % self.dimensions
            vector[idx] += 1.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        return vector.tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)


# =============================================================================
# 2. SAMPLE KNOWLEDGE BASE DOCUMENTS
# =============================================================================
# A mock internal company knowledge base that no general LLM knows about
COMPANY_HANDBOOK_TEXT = """
=== ACME CORP INTERNAL ENGINEERING HANDBOOK (2026) ===

CHAPTER 1: REMOTE WORK AND EQUIPMENT POLICY
Employees at Acme Corp are allocated a $1,500 one-time hardware stipend for home offices.
All equipment must run enterprise disk encryption. Remote team members can work from
any location within a 3-hour timezone offset of UTC-5 (New York time).

CHAPTER 2: CODE REVIEWS AND PULL REQUESTS
Every Pull Request requires at least two approving reviews from senior engineers before merge.
Automated CI test coverage must stay strictly above 85%. Any deployment to the production
cluster happens only on Tuesdays and Thursdays between 10:00 AM and 2:00 PM EST to ensure
full engineering team availability for incident response.

CHAPTER 3: ON-CALL INCIDENT ESCALATION
The on-call engineer must acknowledge P1 alerts within 5 minutes. If no response occurs,
the pager automatically escalates to the Engineering Director after 12 minutes. P1 post-mortems
are strictly blameless and must be published to the wiki within 48 hours of resolution.
"""


# =============================================================================
# 3. BUILD THE RAG PIPELINE
# =============================================================================
def build_rag_chain():
    # Step A: Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )
    docs = text_splitter.create_documents([COMPANY_HANDBOOK_TEXT])
    print(f"[INGESTION] Document split into {len(docs)} searchable chunks.")

    # Step B: Index into local InMemoryVectorStore
    embedding_model = LocalKeywordEmbeddings()
    vector_store = InMemoryVectorStore.from_documents(
        documents=docs,
        embedding=embedding_model,
    )
    # Convert vector store to a retriever (fetches top 3 most relevant chunks)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Step C: Helper to format retrieved documents into a clean string
    def format_docs(retrieved_docs: List[Document]) -> str:
        return "\n\n---\n\n".join(doc.page_content for doc in retrieved_docs)

    # Step D: Construct the RAG Prompt Template
    rag_prompt = ChatPromptTemplate.from_template(
        "You are an assistant answering questions using the provided context.\n"
        "Strict Rule: Answer ONLY based on the context below. If you don't know, say so.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Grounded Answer:"
    )

    llm = get_llm(temperature=0.0)

    # Step E: The Classic RAG LCEL Chain
    # 1. Takes {"question": "..."} as input
    # 2. In parallel:
    #    - context = question | retriever | format_docs
    #    - question = passed through unchanged
    # 3. Formats into rag_prompt -> calls LLM -> parses string
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever


# =============================================================================
# 4. RUN TEST QUERIES
# =============================================================================
def main():
    print("=" * 70)
    print("LANGCHAIN LESSON 4: RETRIEVAL-AUGMENTED GENERATION (RAG)")
    print("=" * 70)

    rag_chain, retriever = build_rag_chain()

    test_questions = [
        "What days and times are production deployments allowed at Acme Corp?",
        "What is the policy and response time for a P1 alert escalation?",
        "How much stipend do remote employees get for home office hardware?",
    ]

    for q in test_questions:
        print("\n" + "=" * 60)
        print(f"USER QUESTION: '{q}'")
        print("=" * 60)

        # Show which context chunks the retriever found
        relevant_chunks = retriever.invoke(q)
        print(f"[RETRIEVER] Found {len(relevant_chunks)} matching chunks:")
        for idx, chunk in enumerate(relevant_chunks, 1):
            snippet = chunk.page_content.replace("\n", " ")[:90]
            print(f"  Chunk {idx}: {snippet}...")

        # Execute full LCEL RAG chain
        answer = rag_chain.invoke(q)
        print(f"\n[AI GROUNDED ANSWER]:\n{answer}")


if __name__ == "__main__":
    main()

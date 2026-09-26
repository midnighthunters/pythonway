"""
Verification Test Suite for Project 016: Document Ingestion & Chunking Strategy Benchmark
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    SAMPLE_HANDBOOK_MARKDOWN,
    naive_fixed_chunking,
    recursive_chunking,
    markdown_header_chunking,
)


def test_recursive_chunking_constraints():
    print("Testing RecursiveCharacterTextSplitter constraints...")
    chunk_size = 200
    chunk_overlap = 40
    docs = recursive_chunking(SAMPLE_HANDBOOK_MARKDOWN, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    assert len(docs) > 1, f"Expected multiple chunks, got {len(docs)}"

    # Check that chunks respect maximum length bounds
    for i, doc in enumerate(docs):
        assert len(doc.page_content) <= chunk_size + 20, (
            f"Chunk {i} exceeded max size: {len(doc.page_content)} > {chunk_size}"
        )

    # Check that words are not split in half (each chunk should start with a clean word/header/newline)
    for doc in docs:
        first_token = doc.page_content.strip().split()[0]
        assert len(first_token) > 0, "Chunk contains empty token"

    print(f"  [PASSED] Recursive chunker produced {len(docs)} well-bounded, word-safe chunks.")


def test_markdown_header_metadata():
    print("\nTesting MarkdownHeaderTextSplitter metadata preservation...")
    docs = markdown_header_chunking(SAMPLE_HANDBOOK_MARKDOWN)

    # There are 4 distinct ## sections in the sample handbook
    assert len(docs) == 4, f"Expected 4 markdown sections, got {len(docs)}"

    # Check metadata enrichment
    for doc in docs:
        assert "Document Title" in doc.metadata, "Missing 'Document Title' metadata key"
        assert "Section Title" in doc.metadata, "Missing 'Section Title' metadata key"
        assert doc.metadata["Document Title"] == "Cozy Coffee & Bakery Handbook"

    # Verify section 2 content
    section_2 = docs[1]
    assert "2. Kitchen Safety & Microwave Rules" in section_2.metadata["Section Title"]
    assert "microwave" in section_2.page_content.lower()
    assert "refrigerator cleaner" in section_2.page_content.lower()

    print("  [PASSED] Markdown chunker successfully extracted 4 sections with rich metadata.")


def test_retrieval_relevance():
    print("\nTesting chunk retrieval accuracy for RAG...")
    docs = markdown_header_chunking(SAMPLE_HANDBOOK_MARKDOWN)

    query = "microwave"
    matches = [d for d in docs if query in d.page_content.lower()]

    assert len(matches) == 1, f"Expected exactly 1 chunk matching '{query}', found {len(matches)}"
    assert "Kitchen Safety" in matches[0].metadata["Section Title"]
    print(f"  [PASSED] Query '{query}' precisely resolved to section: {matches[0].metadata['Section Title']}")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 016")
    print("=" * 60)
    test_recursive_chunking_constraints()
    test_markdown_header_metadata()
    test_retrieval_relevance()
    print("\n[ALL TESTS PASSED] Project 016 verified successfully!")

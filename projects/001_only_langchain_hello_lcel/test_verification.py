"""
Automated Verification Test for Project 001.
Verifies that message types, LCEL chains, and output parsers work as expected.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_llm


def test_lcel_chain_execution():
    llm = get_llm(temperature=0.0)
    prompt = ChatPromptTemplate.from_template("Respond with exactly the single word 'VERIFIED': {query}")
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"query": "Confirm system test"})
    assert "VERIFIED" in result.strip().upper(), f"Expected 'VERIFIED' in response, got: {result}"
    print("✅ test_lcel_chain_execution PASSED!")


def test_batch_execution():
    llm = get_llm(temperature=0.0)
    prompt = ChatPromptTemplate.from_template("What is 1 + {num}? Reply with just the number.")
    chain = prompt | llm | StrOutputParser()

    batch_inputs = [{"num": "1"}, {"num": "2"}]
    results = chain.batch(batch_inputs)
    assert len(results) == 2, f"Expected 2 results, got {len(results)}"
    assert "2" in results[0], f"Expected 2 in first result, got: {results[0]}"
    assert "3" in results[1], f"Expected 3 in second result, got: {results[1]}"
    print("✅ test_batch_execution PASSED!")


if __name__ == "__main__":
    test_lcel_chain_execution()
    test_batch_execution()
    print("🎉 ALL PROJECT 001 AUTOMATED TESTS PASSED!")

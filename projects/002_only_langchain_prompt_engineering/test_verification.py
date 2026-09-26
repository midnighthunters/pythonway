"""
Automated Verification Test for Project 002.
Verifies partial prompt formatting, few-shot generation, and MessagesPlaceholder.
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from config import get_llm


def test_partial_prompt():
    base_prompt = ChatPromptTemplate.from_messages([
        ("system", "You work for {company}."),
        ("human", "Say hello in 3 words: {topic}"),
    ])
    partial_prompt = base_prompt.partial(company="Tesla")
    formatted = partial_prompt.format_messages(topic="cars")
    assert any("Tesla" in msg.content for msg in formatted), "Expected 'Tesla' in formatted messages"
    print("✅ test_partial_prompt PASSED!")


def test_few_shot_prompt():
    examples = [
        {"input": "happy", "sentiment": "POSITIVE"},
        {"input": "sad", "sentiment": "NEGATIVE"},
    ]
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{sentiment}"),
    ])
    few_shot = FewShotChatMessagePromptTemplate(examples=examples, example_prompt=example_prompt)
    prompt = ChatPromptTemplate.from_messages([few_shot, ("human", "{input}")])
    llm = get_llm(temperature=0.0)
    chain = prompt | llm | StrOutputParser()

    res = chain.invoke({"input": "furious"})
    assert "NEGATIVE" in res.upper(), f"Expected NEGATIVE sentiment, got: {res}"
    print("✅ test_few_shot_prompt PASSED!")


def test_messages_placeholder():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use conversation history to answer questions accurately."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{query}"),
    ])
    history = [
        HumanMessage(content="My first name is James and my last name is Bond."),
        AIMessage(content="Pleased to meet you, Mr. Bond."),
    ]
    llm = get_llm(temperature=0.0)
    chain = prompt | llm | StrOutputParser()
    res = chain.invoke({"history": history, "query": "What is my last name?"})
    assert "Bond" in res, f"Expected 'Bond' in response, got: {res}"
    print("✅ test_messages_placeholder PASSED!")


if __name__ == "__main__":
    test_partial_prompt()
    test_few_shot_prompt()
    test_messages_placeholder()
    print("🎉 ALL PROJECT 002 AUTOMATED TESTS PASSED!")

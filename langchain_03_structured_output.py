"""
===============================================================================
LANGCHAIN CONCEPT 3: STRUCTURED OUTPUTS & SCHEMA ENFORCEMENT
===============================================================================

Why Structured Outputs?
-----------------------
Freeform text from LLMs is difficult to parse reliably in production code.
When feeding data into:
  - Databases (SQL, MongoDB)
  - Backend APIs (REST, gRPC)
  - Other automated microservices

You need guaranteed JSON objects conforming to strict schemas and types.

LangChain provides two primary ways to achieve this:
  1. `llm.with_structured_output(PydanticModel)`:
     Uses Groq's underlying tool-calling/JSON schema engine to directly output
     a validated Pydantic object.
  2. `JsonOutputParser` / `PydanticOutputParser`:
     Injects format instructions into the prompt and parses the LLM's raw text
     response into Python dictionaries or Pydantic instances.

In this lesson:
  1. Define a rich Pydantic model (`CandidateProfile`).
  2. Extract structured candidate data from an unstructured email.
  3. Validate fields, types, and nested lists automatically.
  4. Compare `with_structured_output` vs `JsonOutputParser`.
===============================================================================
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import get_llm


# =============================================================================
# 1. DEFINE PYDANTIC SCHEMA
# =============================================================================
class CandidateProfile(BaseModel):
    """Structured information extracted from a job applicant's profile."""
    full_name: str = Field(description="The applicant's full legal name")
    current_role: str = Field(description="Current or most recent job title")
    years_of_experience: int = Field(description="Total years of professional experience as an integer")
    primary_skills: List[str] = Field(description="Top 3 to 5 technical skills or programming languages")
    current_company: Optional[str] = Field(default=None, description="Current employer if mentioned")
    open_to_remote: bool = Field(description="True if the candidate is open to remote work, else False")
    summary: str = Field(description="A concise 1-sentence professional summary")


# Unstructured applicant text from an inbound email or message
SAMPLE_APPLICANT_EMAIL = """
Hey Hiring Team!
My name is Sarah Connor. For the past 4 years I've been working at Cyberdyne Systems
as a Senior DevOps & Cloud Engineer, and before that I did 3 years as a Linux Systems Admin.
I specialize heavily in Kubernetes, Terraform, Docker, Python, and AWS architecture.
I'm based in Austin, TX, but I'm only looking for fully remote opportunities right now.
Looking forward to hearing from you!
"""


# =============================================================================
# 2. METHOD A: llm.with_structured_output(PydanticModel)
# =============================================================================
def demo_with_structured_output():
    print("=" * 70)
    print("METHOD A: llm.with_structured_output(PydanticModel)")
    print("=" * 70)
    print("Directly returns a typed Pydantic instance with validated fields:\n")

    llm = get_llm(temperature=0.0)

    # Bind the Pydantic schema to the model
    structured_llm = llm.with_structured_output(CandidateProfile)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI recruitment assistant. Extract structured candidate details from the text."),
        ("human", "{input_text}"),
    ])

    chain = prompt | structured_llm

    # Execute
    candidate: CandidateProfile = chain.invoke({"input_text": SAMPLE_APPLICANT_EMAIL})

    print(f"Extracted Object Type: {type(candidate)}")
    print(f" - Full Name           : {candidate.full_name}")
    print(f" - Current Role        : {candidate.current_role}")
    print(f" - Current Company     : {candidate.current_company}")
    print(f" - Total Experience    : {candidate.years_of_experience} years")
    print(f" - Primary Skills      : {', '.join(candidate.primary_skills)}")
    print(f" - Remote Work Eligible: {candidate.open_to_remote}")
    print(f" - Summary             : {candidate.summary}")

    # You can directly dump to JSON or Python dict!
    print(f"\nSerialized JSON Dictionary:\n{candidate.model_dump()}")


# =============================================================================
# 3. METHOD B: JsonOutputParser WITH PROMPT INSTRUCTIONS
# =============================================================================
def demo_json_output_parser():
    print("\n" + "=" * 70)
    print("METHOD B: JsonOutputParser (PROMPT-DRIVEN JSON EXTRACTION)")
    print("=" * 70)
    print("Injects JSON schema instructions into the prompt and returns a dict:\n")

    llm = get_llm(temperature=0.0)
    parser = JsonOutputParser(pydantic_object=CandidateProfile)

    # parser.get_format_instructions() injects exact schema rules into the prompt
    prompt = ChatPromptTemplate.from_template(
        "Extract candidate profile information from this text:\n{input_text}\n\n"
        "Formatting Instructions:\n{format_instructions}"
    )

    chain = prompt | llm | parser

    result = chain.invoke({
        "input_text": SAMPLE_APPLICANT_EMAIL,
        "format_instructions": parser.get_format_instructions(),
    })

    print(f"Extracted Type: {type(result)} (Python dict)")
    print(f"Result:\n{result}")


# =============================================================================
# MAIN RUNNER
# =============================================================================
def main():
    print("=" * 70)
    print("LANGCHAIN LESSON 3: STRUCTURED OUTPUTS & PYDANTIC VALIDATION")
    print("=" * 70)

    demo_with_structured_output()
    demo_json_output_parser()


if __name__ == "__main__":
    main()

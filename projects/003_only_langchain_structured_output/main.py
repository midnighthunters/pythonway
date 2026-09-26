"""
===============================================================================
PROJECT 003: STRUCTURED OUTPUTS & STRICT PYDANTIC SCHEMA ENFORCEMENT
Stage 1: Pure Fundamentals | Difficulty: 2.0 / 10 (Beginner)
===============================================================================

Core Concepts Demonstrated:
1. Pydantic v2 Models: Declaring typed fields, descriptions, and validators.
2. Schema Guardrails: Ensuring outputs adhere strictly to programmatic invariants.
3. with_structured_output(): Model-native schema enforcement via tool calling.
4. JsonOutputParser: Prompt-based schema extraction with explicit instructions.
===============================================================================
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. DEFINE PYDANTIC SCHEMA WITH GUARDRAIL VALIDATION
# =============================================================================
class IncidentReport(BaseModel):
    """Structured report extracted from an unstructured system alert message."""
    service_name: str = Field(description="The primary microservice affected, e.g. 'auth-service'")
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(
        description="The alert triage tier strictly chosen from: LOW, MEDIUM, HIGH, CRITICAL"
    )
    error_code: Optional[int] = Field(default=None, description="HTTP or internal error code if specified")
    root_cause_hypothesis: str = Field(description="A concise 1-sentence technical diagnosis")
    impacted_regions: List[str] = Field(description="List of data centers or cloud regions affected")
    confidence_score: float = Field(description="Numeric confidence from 0.0 to 1.0 in this triage diagnosis")

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Schema Guardrail: Enforces confidence within valid probability bounds."""
        if not (0.0 <= v <= 1.0):
            raise ValueError(f"Confidence score must be strictly between 0.0 and 1.0, got: {v}")
        return round(v, 2)


# Sample unstructured real-world alert from Slack/PagerDuty
SAMPLE_ALERT_MESSAGE = """
[URGENT INCIDENT 9042]
Payments gateway (checkout-payment-api) is failing across us-east-1 and eu-central-1!
Over 45% of user checkout requests are receiving HTTP 504 Gateway Timeout errors.
Engineers suspect connection pool exhaustion on the primary PostgreSQL cluster after the v3.4 migration.
Customer transactions are completely stalled.
"""


def demo_with_structured_output():
    """Method A: Native tool-calling schema mode."""
    print("=" * 70)
    print("METHOD A: llm.with_structured_output(IncidentReport)")
    print("=" * 70)
    print("Directly produces a validated Pydantic model instance:\n")

    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(IncidentReport)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an automated Site Reliability Engineering triage agent."),
        ("human", "Analyze this alert and extract a structured incident report:\n\n{alert}"),
    ])

    chain = prompt | structured_llm

    print(f"Parsing Alert via with_structured_output()...")
    report: IncidentReport = chain.invoke({"alert": SAMPLE_ALERT_MESSAGE})

    print(f"\n[PARSED PYDANTIC OBJECT]:")
    print(f" - Service Name   : {report.service_name}")
    print(f" - Severity Tier  : {report.severity}")
    print(f" - Error Code     : {report.error_code}")
    print(f" - Root Cause     : {report.root_cause_hypothesis}")
    print(f" - Regions        : {report.impacted_regions}")
    print(f" - Confidence     : {report.confidence_score}")
    print(f"\nSerialized Dict:\n{report.model_dump()}")
    print("-" * 70)


def demo_json_output_parser():
    """Method B: Prompt-driven schema formatting instructions."""
    print("\n" + "=" * 70)
    print("METHOD B: JsonOutputParser(pydantic_object=IncidentReport)")
    print("=" * 70)
    print("Injects JSON schema instructions into the prompt text:\n")

    llm = get_llm(temperature=0.0)
    parser = JsonOutputParser(pydantic_object=IncidentReport)

    prompt = ChatPromptTemplate.from_template(
        "You are an SRE triage assistant. Extract structured incident data from this alert:\n"
        "{alert}\n\n"
        "{format_instructions}"
    )

    chain = prompt | llm | parser

    print("Parsing Alert via JsonOutputParser()...")
    parsed_json = chain.invoke({
        "alert": SAMPLE_ALERT_MESSAGE,
        "format_instructions": parser.get_format_instructions(),
    })

    print(f"\n[PARSED JSON DICTIONARY]:")
    for key, value in parsed_json.items():
        print(f" - {key}: {value}")
    print("=" * 70)


def main():
    print("*" * 70)
    print("PROJECT 003: STRUCTURED OUTPUTS & PYDANTIC SCHEMA ENFORCEMENT")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    demo_with_structured_output()
    demo_json_output_parser()
    print("\n[SUCCESS] Project 003 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()

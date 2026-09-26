"""
Automated Verification Test for Project 003.
Verifies Pydantic extraction, schema guardrails, and validation errors.
"""

from typing import Literal
from pydantic import BaseModel, Field, ValidationError
from config import get_llm


class UserAccount(BaseModel):
    username: str
    role: Literal["ADMIN", "DEVELOPER", "GUEST"]
    quota_limit: int = Field(ge=0, le=1000)


def test_structured_output_extraction():
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(UserAccount)
    res: UserAccount = structured_llm.invoke("Create an account for user 'alice' with role DEVELOPER and quota limit 500.")

    assert isinstance(res, UserAccount), f"Expected UserAccount instance, got {type(res)}"
    assert res.username.lower() == "alice", f"Expected username 'alice', got {res.username}"
    assert res.role == "DEVELOPER", f"Expected role 'DEVELOPER', got {res.role}"
    assert res.quota_limit == 500, f"Expected quota 500, got {res.quota_limit}"
    print("✅ test_structured_output_extraction PASSED!")


def test_schema_guardrail_validation():
    # Verify that Pydantic rejects invalid roles
    try:
        UserAccount(username="bad_user", role="SUPERUSER", quota_limit=10)
        assert False, "Expected ValidationError for invalid role"
    except ValidationError:
        print("✅ test_schema_guardrail_validation (Invalid Role Blocked) PASSED!")

    # Verify that Pydantic rejects negative quotas
    try:
        UserAccount(username="bad_user", role="ADMIN", quota_limit=-5)
        assert False, "Expected ValidationError for negative quota"
    except ValidationError:
        print("✅ test_schema_guardrail_validation (Negative Quota Blocked) PASSED!")


if __name__ == "__main__":
    test_structured_output_extraction()
    test_schema_guardrail_validation()
    print("🎉 ALL PROJECT 003 AUTOMATED TESTS PASSED!")

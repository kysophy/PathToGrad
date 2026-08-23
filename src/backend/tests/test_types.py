from app.deterministic.types import (
    RISK_SEVERITY,
    CoursePrimaryStatus,
    ExclusionReason,
    RiskCode,
    SelectionReason,
    TermType,
    ToolStatus,
)
from app.schemas import enums


def test_risk_code_is_the_same_object():
    assert RiskCode is enums.RiskCode


def test_reexports_are_identity():
    assert TermType is enums.TermType
    assert ToolStatus is enums.ToolStatus
    assert CoursePrimaryStatus is enums.CoursePrimaryStatus
    assert SelectionReason is enums.SelectionReason
    assert ExclusionReason is enums.ExclusionReason
    assert RISK_SEVERITY is enums.RISK_SEVERITY

"""Deterministic planning engine (Part 3).

Trâm imports the functions below. Khoa imports `find_prerequisite_cycles`.
Legacy modules `prerequisite_checker` and `graduation_progress` are unchanged.
"""

from app.deterministic.cadence import (
    CadenceMismatchError,
    assert_offered_in,
    is_offered_in,
    position_of,
)
from app.deterministic.catalog import get_course_catalog
from app.deterministic.conflicts import detect_conflicts
from app.deterministic.credit_policy import validate_credit_load
from app.deterministic.generator import generate_semester_plan
from app.deterministic.prerequisites import (
    check_prerequisites,
    find_prerequisite_cycles,
)
from app.deterministic.progress import get_graduation_progress
from app.deterministic.retakes import rank_retakes
from app.deterministic.risks import detect_risks
from app.deterministic.types import (
    RISK_SEVERITY,
    CoursePrimaryStatus,
    ExclusionReason,
    RiskCode,
    SelectionReason,
    TermType,
    ToolStatus,
)

__all__ = [
    "CadenceMismatchError",
    "CoursePrimaryStatus",
    "ExclusionReason",
    "RISK_SEVERITY",
    "RiskCode",
    "SelectionReason",
    "TermType",
    "ToolStatus",
    "assert_offered_in",
    "check_prerequisites",
    "detect_conflicts",
    "detect_risks",
    "find_prerequisite_cycles",
    "generate_semester_plan",
    "get_course_catalog",
    "get_graduation_progress",
    "is_offered_in",
    "position_of",
    "rank_retakes",
    "validate_credit_load",
]

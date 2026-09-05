"""Templates must name only engine codes and cover the main reasons."""

from app.llm.templates import explain_course, explain_plan
from app.schemas.enums import ExclusionReason, SelectionReason
from app.schemas.tools import GeneratedPlan, PlanExclusion, PlanItem, Risk
from app.schemas.enums import RiskCode, RiskSeverity


def test_assigned_and_backlog_sentences_exist():
    plan = GeneratedPlan(
        student_id="S1",
        term_id="TERM-2026-1",
        items=[
            PlanItem(
                course_id="a",
                course_code="CSC10004",
                section_id="s1",
                credits=4,
                selection_reason=SelectionReason.ASSIGNED_THIS_SEMESTER,
            ),
            PlanItem(
                course_id="b",
                course_code="CSC10012",
                section_id="s2",
                credits=4,
                selection_reason=SelectionReason.BACKLOG_FROM_SEMESTER_N,
            ),
        ],
        total_credits=8,
        course_count=2,
    )
    text = explain_plan(plan)
    assert "CSC10004" in text
    assert "assigned this programme semester" in text
    assert "CSC10012" in text
    assert "backlog" in text


def test_cap_and_missing_offering_sentences_exist():
    plan = GeneratedPlan(
        student_id="S1",
        term_id="TERM-2026-1",
        exclusions=[
            PlanExclusion(
                course_id="x",
                course_code="CSC13001",
                reason=ExclusionReason.DROPPED_NOT_OFFERED,
            ),
            PlanExclusion(
                course_id="y",
                course_code="BAA00021",
                reason=ExclusionReason.DEFERRED_CREDIT_CAP,
            ),
        ],
    )
    text = explain_plan(plan)
    assert "CSC13001" in text
    assert "not offered" in text
    assert "BAA00021" in text
    assert "cap" in text


def test_risk_line_keeps_engine_message():
    plan = GeneratedPlan(student_id="S1", term_id="TERM-2026-1")
    risk = Risk(
        code=RiskCode.GPA_BELOW_THRESHOLD,
        severity=RiskSeverity.MEDIUM,
        message="GPA 4.9 is below the warning threshold 5.0.",
        course_codes=[],
    )
    text = explain_plan(plan, [risk])
    assert "GPA_BELOW_THRESHOLD" in text
    assert "4.9" in text


def test_course_template_says_when_brief_is_missing():
    text = explain_course("CSC10004", name_en="Data Structures and Algorithms")
    assert "CSC10004" in text
    assert "do not have a description" in text
    assert "illustrative, not the official syllabus" in text


def test_course_template_uses_vietnamese_then_english():
    text = explain_course(
        "CSC10004",
        name_vi="Cấu trúc dữ liệu và giải thuật",
        name_en="Data Structures and Algorithms",
        brief="Lists, stacks, trees, and graphs.",
    )
    assert "CSC10004 — Cấu trúc dữ liệu và giải thuật (Data Structures and Algorithms)" in text
    assert "illustrative, not the official syllabus" in text


def test_plan_template_uses_vietnamese_then_english_when_names_given():
    plan = GeneratedPlan(
        student_id="S1",
        term_id="TERM-2026-1",
        items=[
            PlanItem(
                course_id="a",
                course_code="CSC10004",
                section_id="s1",
                credits=4,
                selection_reason=SelectionReason.ASSIGNED_THIS_SEMESTER,
            ),
        ],
        total_credits=4,
        course_count=1,
    )
    text = explain_plan(
        plan,
        names_en={"CSC10004": "Data Structures and Algorithms"},
        names_vi={"CSC10004": "Cấu trúc dữ liệu và giải thuật"},
    )
    assert "CSC10004 — Cấu trúc dữ liệu và giải thuật (Data Structures and Algorithms)" in text

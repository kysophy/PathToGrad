"""Canned Stage-3 / chat sentences. Keyed on engine enums, not model opinion."""

from __future__ import annotations

from app.schemas.enums import ExclusionReason, SelectionReason
from app.schemas.tools import GeneratedPlan, Risk

_REASON = {
    SelectionReason.ASSIGNED_THIS_SEMESTER: (
        "assigned this programme semester and not yet passed"
    ),
    SelectionReason.BACKLOG_FROM_SEMESTER_N: (
        "a backlog from an earlier semester"
    ),
    SelectionReason.ELECTIVE_FILL: (
        "an elective fill so the load meets the CLC minimum"
    ),
    SelectionReason.RETAKE_AFTER_FAIL: "a retake after a fail",
    SelectionReason.RETAKE_IMPROVEMENT: "an optional improvement retake",
}

_EXCLUSION = {
    ExclusionReason.DEFERRED_CREDIT_CAP: "the credit or course-count cap",
    ExclusionReason.DROPPED_PREREQ_BLOCKED: "a missing or unsatisfied prerequisite",
    ExclusionReason.DROPPED_NOT_OFFERED: "it is not offered this term",
    ExclusionReason.DROPPED_ALL_SECTIONS_CONFLICT: (
        "every section clashes with something already on the plan"
    ),
}

GREETING = (
    "I can help with this term's study plan, catalog notes "
    "(what a course is about), and academic risk. "
    "I do not register you at HCMUS — you still add, drop, save Draft, "
    "and submit. Try “Generate my plan” or “What is CSC10004?”"
)

REFUSE = (
    "I only help with this term's plan, catalog course notes, and academic "
    "risk. I cannot register you or answer that."
)


def _label(
    course_code: str,
    names_en: dict[str, str] | None = None,
    names_vi: dict[str, str] | None = None,
) -> str:
    en = (names_en or {}).get(course_code)
    vi = (names_vi or {}).get(course_code)
    if vi and en:
        return f"{course_code} — {vi} ({en})"
    if vi:
        return f"{course_code} — {vi}"
    if en:
        return f"{course_code} — {en}"
    return course_code


def explain_plan(
    plan: GeneratedPlan,
    risks: list[Risk] | None = None,
    *,
    names_en: dict[str, str] | None = None,
    names_vi: dict[str, str] | None = None,
) -> str:
    risks = risks or []
    lines = [
        "Here is the engine plan. This is a suggestion, not a registration."
    ]
    if not plan.items:
        lines.append(
            "The engine did not place any courses. Read the warnings below."
        )
    for item in plan.items:
        why = _REASON.get(item.selection_reason, item.selection_reason.value)
        label = _label(item.course_code, names_en, names_vi)
        lines.append(f"- {label} ({item.credits} credits): {why}.")
    for exclusion in plan.exclusions:
        why = _EXCLUSION.get(exclusion.reason, exclusion.reason.value)
        label = _label(exclusion.course_code, names_en, names_vi)
        lines.append(f"- {label} was not placed because of {why}.")
    if plan.total_credits or plan.course_count:
        lines.append(
            f"Total: {plan.total_credits} credits, {plan.course_count} courses."
        )
    for warning in plan.warnings:
        lines.append(f"Warning: {warning}")
    for risk in risks:
        codes = ", ".join(risk.course_codes) if risk.course_codes else ""
        suffix = f" ({codes})" if codes else ""
        lines.append(f"Risk {risk.code.value}{suffix}: {risk.message}")
    return "\n".join(lines)


def explain_course(
    course_code: str,
    *,
    name_en: str | None = None,
    name_vi: str | None = None,
    credits: int | None = None,
    brief: str | None = None,
    prereq_codes: list[str] | None = None,
    assigned_semester: int | None = None,
    offered: bool | None = None,
    blocked: bool | None = None,
    primary_status: str | None = None,
) -> str:
    if name_vi and name_en:
        title = f"{name_vi} ({name_en})"
    elif name_vi:
        title = name_vi
    elif name_en:
        title = name_en
    else:
        title = course_code
    bits = [f"{course_code} — {title}."]
    if credits is not None:
        bits.append(f"It is {credits} credits.")
    if assigned_semester is not None:
        bits.append(f"Curriculum slot: programme semester {assigned_semester}.")
    if primary_status:
        bits.append(f"For you this term it is {primary_status}.")
    if offered is False:
        bits.append("It is not offered this calendar term.")
    if blocked:
        bits.append("A prerequisite is blocking it.")
    if prereq_codes:
        bits.append("Prerequisites: " + ", ".join(prereq_codes) + ".")
    if brief:
        bits.append(brief)
    else:
        bits.append(
            "We do not have a description for this course. "
            "This is not an official HCMUS syllabus."
        )
    bits.append("This note is illustrative, not the official syllabus.")
    return " ".join(bits)


def unknown_course(course_code: str) -> str:
    return (
        f"I do not have {course_code} in this demo catalog (GEN+SE). "
        "I will not invent a course."
    )

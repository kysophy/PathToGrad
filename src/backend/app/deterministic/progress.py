"""Graduation progress tracker (A-13).

Two independent conditions: every mandatory (Core) course passed, **and**
earned credits ≥ curriculum.required_credits. Only Passed attempts with a
grade count. GPA uses the latest attempt per course, not the best one.
"""

from __future__ import annotations

from app.deterministic.ports import PlanningRepos
from app.deterministic.types import ToolStatus
from app.schemas.tools import GraduationProgress


def _grade(value) -> float | None:
    if value is None:
        return None
    return float(value)


def get_graduation_progress(
    student_id: str,
    *,
    repos: PlanningRepos,
) -> GraduationProgress:
    profile = repos.students.get_with_policy(student_id)
    if profile is None:
        return GraduationProgress(
            student_id=student_id,
            earned_credits=0,
            required_credits=0,
            remaining_credits=0,
            mandatory_passed=False,
            credit_requirement_met=False,
            status=ToolStatus.UNCERTAIN,
            warnings=[f"Student {student_id} was not found."],
        )
    if profile.curriculum is None or profile.curriculum_id is None:
        return GraduationProgress(
            student_id=student_id,
            earned_credits=0,
            required_credits=0,
            remaining_credits=0,
            mandatory_passed=False,
            credit_requirement_met=False,
            status=ToolStatus.UNCERTAIN,
            warnings=["Student has no curriculum."],
        )

    required_credits = profile.curriculum.required_credits
    mandatory = repos.curriculum.list_mandatory_courses(
        profile.curriculum_id, profile.spec_code
    )
    mandatory_codes = {course.course_code: course for course in mandatory}

    record = repos.attempts.get_record(student_id)
    latest = []
    if record is not None:
        latest = repos.attempts.latest_per_course(record.record_id)

    warnings: list[str] = []
    earned = 0
    weighted = 0.0
    weight = 0
    passed_codes: set[str] = set()

    for attempt in latest:
        course = repos.courses.get_by_id(attempt.course_id)
        if course is None:
            continue
        grade = _grade(attempt.grade)
        if attempt.result_status == "InProgress":
            continue
        if attempt.result_status == "Passed" and grade is None:
            warnings.append(
                f"{course.course_code}: Passed attempt has no grade, so it is not counted."
            )
            continue
        if grade is not None:
            weighted += grade * course.credits
            weight += course.credits
        if attempt.result_status == "Passed" and grade is not None:
            earned += course.credits
            passed_codes.add(course.course_code)

    missing = sorted(
        code for code in mandatory_codes if code not in passed_codes
    )
    remaining = max(required_credits - earned, 0)
    credit_met = earned >= required_credits
    mandatory_passed = missing == []
    gpa = round(weighted / weight, 2) if weight else None
    status = ToolStatus.UNCERTAIN if warnings else ToolStatus.OK
    return GraduationProgress(
        student_id=student_id,
        earned_credits=earned,
        required_credits=required_credits,
        remaining_credits=remaining,
        mandatory_passed=mandatory_passed,
        credit_requirement_met=credit_met,
        missing_required_courses=missing,
        gpa=gpa,
        completed=mandatory_passed and credit_met,
        status=status,
        warnings=warnings,
    )

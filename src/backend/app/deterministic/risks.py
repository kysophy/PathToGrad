"""Academic risk detector (A-18). Eleven codes, no invented cohort statistics."""

from __future__ import annotations

from app.deterministic.catalog import get_course_catalog
from app.deterministic.constants import (
    BACKLOG_STALE_SEMESTERS,
    ELECTIVE_POOL_EXHAUSTED,
    GPA_WARNING_THRESHOLD,
    NEAR_GRADUATION_SEMESTER,
)
from app.deterministic.ports import PlanningRepos
from app.deterministic.progress import get_graduation_progress
from app.deterministic.types import (
    CoursePrimaryStatus,
    ExclusionReason,
    RISK_SEVERITY,
    RiskCode,
    SelectionReason,
    ToolStatus,
)
from app.schemas.tools import GeneratedPlan, Risk


def _risk(code: RiskCode, message: str, course_codes: list[str] | None = None) -> Risk:
    return Risk(
        code=code,
        severity=RISK_SEVERITY[code],
        message=message,
        course_codes=course_codes or [],
    )


def detect_risks(
    student_id: str,
    plan: GeneratedPlan | None = None,
    *,
    repos: PlanningRepos,
    term_id: str | None = None,
) -> list[Risk]:
    profile = repos.students.get_with_policy(student_id)
    risks: list[Risk] = []
    if profile is None:
        return risks

    if profile.current_semester >= NEAR_GRADUATION_SEMESTER and not profile.spec_code:
        risks.append(
            _risk(
                RiskCode.SPECIALIZATION_NOT_SET,
                "Student is at semester 7 or beyond with no specialization set.",
            )
        )

    progress = get_graduation_progress(student_id, repos=repos)
    if (
        progress.gpa is not None
        and progress.status != ToolStatus.UNCERTAIN
        and progress.gpa < GPA_WARNING_THRESHOLD
    ):
        risks.append(
            _risk(
                RiskCode.GPA_BELOW_THRESHOLD,
                f"GPA {progress.gpa} is below the warning threshold "
                f"{GPA_WARNING_THRESHOLD}.",
            )
        )

    record = repos.attempts.get_record(student_id)
    latest = []
    if record is not None:
        latest = repos.attempts.latest_per_course(record.record_id)

    curr_rows = {}
    if profile.curriculum_id:
        curr_rows = {
            course.course_id: row
            for row, course in repos.curriculum.list_courses_for_student(
                profile.curriculum_id, profile.spec_code
            )
        }

    failed_twice = []
    failed_unretaken = []
    for attempt in latest:
        course = repos.courses.get_by_id(attempt.course_id)
        if course is None:
            continue
        if attempt.result_status == "Failed" and attempt.attempt_number >= 2:
            failed_twice.append(course.course_code)
        elif (
            attempt.result_status == "Failed"
            and attempt.attempt_number < 2
            and profile.current_semester >= NEAR_GRADUATION_SEMESTER
        ):
            failed_unretaken.append(course.course_code)

    if failed_twice:
        risks.append(
            _risk(
                RiskCode.NO_RETAKE_REMAINING,
                "Course failed twice — cannot be attempted again.",
                failed_twice,
            )
        )
    if failed_unretaken:
        risks.append(
            _risk(
                RiskCode.FAILED_UNRETAKEN_LATE,
                "A failed course is still unretaken near graduation.",
                failed_unretaken,
            )
        )

    stale = []
    for course_id, row in curr_rows.items():
        if row.requirement_type != "Core":
            continue
        if profile.current_semester - row.assigned_semester < BACKLOG_STALE_SEMESTERS:
            continue
        attempt = next((item for item in latest if item.course_id == course_id), None)
        passed = (
            attempt is not None
            and attempt.result_status == "Passed"
            and attempt.grade is not None
        )
        if not passed:
            course = repos.courses.get_by_id(course_id)
            if course is not None:
                stale.append(course.course_code)
    if stale:
        risks.append(
            _risk(
                RiskCode.BACKLOG_STALE,
                "Mandatory backlog is two or more semesters old.",
                stale,
            )
        )

    resolved_term = term_id or (plan.term_id if plan is not None else None)
    if resolved_term:
        catalog = get_course_catalog(student_id, resolved_term, repos=repos)
        assigned = [
            course
            for course in catalog.courses
            if course.primary_status == CoursePrimaryStatus.ASSIGNED
        ]
        assigned_credits = sum(course.credits for course in assigned)
        track = profile.program.track if profile.program is not None else None
        if track is not None and assigned_credits > track.max_credits_per_term:
            risks.append(
                _risk(
                    RiskCode.ASSIGNED_OVER_CAP,
                    "Mandatory courses alone exceed the credit cap.",
                    [course.course_code for course in assigned],
                )
            )
        blocked = [
            course.course_code
            for course in assigned
            if course.blocked
        ]
        if blocked:
            risks.append(
                _risk(
                    RiskCode.PREREQ_BLOCKED,
                    "An assigned course has an unmet prerequisite.",
                    blocked,
                )
            )
        missing_offering = [
            course.course_code
            for course in catalog.courses
            if course.is_mandatory
            and course.primary_status
            in {CoursePrimaryStatus.ASSIGNED, CoursePrimaryStatus.BACKLOG}
            and course.not_offered
        ]
        if missing_offering:
            risks.append(
                _risk(
                    RiskCode.COURSE_NOT_OFFERED,
                    "A mandatory course has no offering this term.",
                    missing_offering,
                )
            )

    if plan is None:
        return risks

    track = profile.program.track if profile.program is not None else None
    if track is not None:
        if plan.total_credits > track.max_credits_per_term:
            risks.append(
                _risk(
                    RiskCode.LOAD_OVER_CAP,
                    "Total plan credits are above the maximum.",
                    [item.course_code for item in plan.items],
                )
            )
        elective_exhausted_under_min = (
            plan.total_credits < track.min_credits_per_term
            and any(ELECTIVE_POOL_EXHAUSTED in text for text in plan.warnings)
        )
        if elective_exhausted_under_min:
            risks.append(
                _risk(
                    RiskCode.LOAD_UNDER_MIN,
                    "Below the credit minimum after the elective pool was exhausted.",
                    [item.course_code for item in plan.items],
                )
            )
        if (
            plan.course_count < track.min_courses
            and any(ELECTIVE_POOL_EXHAUSTED in text for text in plan.warnings)
        ):
            risks.append(
                _risk(
                    RiskCode.COURSE_COUNT_UNDER_MIN,
                    "Fewer than the minimum number of courses after top-up.",
                    [item.course_code for item in plan.items],
                )
            )

    if any(
        item.reason == ExclusionReason.DROPPED_ALL_SECTIONS_CONFLICT
        for item in plan.exclusions
    ):
        risks.append(
            _risk(
                RiskCode.TIMETABLE_CONFLICT,
                "A conflict forced a substitution or a drop.",
                [
                    item.course_code
                    for item in plan.exclusions
                    if item.reason == ExclusionReason.DROPPED_ALL_SECTIONS_CONFLICT
                ],
            )
        )

    improvement = [
        item.course_code
        for item in plan.items
        if item.selection_reason == SelectionReason.RETAKE_IMPROVEMENT
    ]
    if improvement:
        risks.append(
            _risk(
                RiskCode.RETAKE_REPLACES_GRADE,
                "Retaking replaces the grade permanently, even if worse.",
                improvement,
            )
        )

    return risks

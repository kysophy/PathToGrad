"""Course catalog + per-student status (A-10).

Exactly one primary status per curriculum course, plus `blocked` and
`not_offered` overlays. Recommended courses (UI) are Assigned + Backlog.
"""

from __future__ import annotations

from app.deterministic.cadence import is_offered_in
from app.deterministic.ports import PlanningRepos
from app.deterministic.prerequisites import check_prerequisites
from app.deterministic.types import CoursePrimaryStatus, ToolStatus
from app.schemas.tools import CatalogCourse, CatalogFilters, CatalogResult


def _latest_by_course(repos: PlanningRepos, student_id: str) -> dict:
    record = repos.attempts.get_record(student_id)
    if record is None:
        return {}
    return {item.course_id: item for item in repos.attempts.latest_per_course(record.record_id)}


def _is_passed(attempt) -> bool:
    if attempt is None:
        return False
    if attempt.result_status != "Passed":
        return False
    return attempt.grade is not None


def _primary_status(
    *,
    is_mandatory: bool,
    assigned_semester: int,
    current_semester: int,
    passed: bool,
    retake_eligible: bool,
) -> CoursePrimaryStatus:
    if passed:
        if retake_eligible:
            return CoursePrimaryStatus.RETAKE
        if not is_mandatory:
            return CoursePrimaryStatus.ELECTIVE
        # Frozen enum has no Completed — keep completed mandatory out of
        # Recommended (Assigned + Backlog) by labelling them Future.
        return CoursePrimaryStatus.FUTURE
    if not is_mandatory:
        return CoursePrimaryStatus.ELECTIVE
    if assigned_semester == current_semester:
        return CoursePrimaryStatus.ASSIGNED
    if assigned_semester < current_semester:
        return CoursePrimaryStatus.BACKLOG
    return CoursePrimaryStatus.FUTURE


def get_course_catalog(
    student_id: str,
    term_id: str,
    filters: CatalogFilters | None = None,
    *,
    repos: PlanningRepos,
) -> CatalogResult:
    warnings: list[str] = []
    profile = repos.students.get_with_policy(student_id)
    term = repos.offerings.get_term(term_id)
    if profile is None:
        return CatalogResult(
            student_id=student_id,
            term_id=term_id,
            status=ToolStatus.UNCERTAIN,
            warnings=[f"Student {student_id} was not found."],
        )
    if profile.curriculum_id is None or profile.curriculum is None:
        return CatalogResult(
            student_id=student_id,
            term_id=term_id,
            status=ToolStatus.UNCERTAIN,
            warnings=["Student has no curriculum."],
        )
    if term is None:
        return CatalogResult(
            student_id=student_id,
            term_id=term_id,
            status=ToolStatus.UNCERTAIN,
            warnings=[f"Academic term {term_id} was not found."],
        )

    rows = repos.curriculum.list_courses_for_student(
        profile.curriculum_id, profile.spec_code
    )
    latest = _latest_by_course(repos, student_id)
    course_ids = [course.course_id for _, course in rows]
    prereq_results = {
        item.course_id: item
        for item in check_prerequisites(student_id, course_ids, repos=repos)
    }

    courses: list[CatalogCourse] = []
    for row, course in rows:
        attempt = latest.get(course.course_id)
        passed = _is_passed(attempt)
        attempt_count = attempt.attempt_number if attempt is not None else 0
        cadence_ok = is_offered_in(row.assigned_semester, term.term_type)
        offering = repos.offerings.get_active_offering(course.course_id, term_id)
        not_offered = (not cadence_ok) or offering is None
        retake_eligible = passed and (not not_offered) and attempt_count < 2
        is_mandatory = row.requirement_type == "Core"
        prereq = prereq_results.get(course.course_id)
        blocked = False
        if prereq is not None:
            if prereq.satisfied is False or prereq.satisfied is None:
                # No configured prerequisites → satisfied True. Uncertain or unmet → overlay.
                if prereq.prerequisites:
                    blocked = True
            if prereq.status == ToolStatus.UNCERTAIN:
                warnings.extend(
                    f"{course.course_code}: {text}" for text in prereq.warnings
                )

        primary = _primary_status(
            is_mandatory=is_mandatory,
            assigned_semester=row.assigned_semester,
            current_semester=profile.current_semester,
            passed=passed,
            retake_eligible=retake_eligible,
        )
        courses.append(
            CatalogCourse(
                course_id=course.course_id,
                course_code=course.course_code,
                name_vi=course.name_vi,
                name_en=course.name_en,
                credits=course.credits,
                assigned_semester=row.assigned_semester,
                is_mandatory=is_mandatory,
                spec_code=row.spec_code,
                primary_status=primary,
                blocked=blocked,
                not_offered=not_offered,
            )
        )

    filters = filters or CatalogFilters()
    if filters.primary_status is not None:
        courses = [
            item for item in courses if item.primary_status == filters.primary_status
        ]
    if filters.offered_only:
        courses = [item for item in courses if not item.not_offered]

    status = ToolStatus.WARNING if warnings else ToolStatus.OK
    return CatalogResult(
        student_id=student_id,
        term_id=term_id,
        courses=courses,
        status=status,
        warnings=list(dict.fromkeys(warnings)),
    )

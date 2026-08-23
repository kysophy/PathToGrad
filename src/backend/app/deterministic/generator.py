"""Semester plan generator (A-16). Sole producer of plan content.

Greedy fill: Assigned → Backlog (oldest first) → Elective (soft-lock top-up)
→ improvement Retakes last. The LLM never generates, filters, or edits this.
"""

from __future__ import annotations

from app.deterministic.cadence import is_offered_in
from app.deterministic.catalog import get_course_catalog
from app.deterministic.conflicts import detect_conflicts
from app.deterministic.constants import ELECTIVE_POOL_EXHAUSTED
from app.deterministic.ports import PlanningRepos
from app.deterministic.types import (
    CoursePrimaryStatus,
    ExclusionReason,
    SelectionReason,
    ToolStatus,
)
from app.schemas.enums import GenerationMode
from app.schemas.tools import (
    CatalogCourse,
    GeneratedPlan,
    PlanExclusion,
    PlanItem,
    PlanRequest,
    TimetableSlot,
)

_PORTAL_CAP_WARNING = (
    "Maximum credits reached — please reconsider your selection."
)


def _pool_exhausted(
    placeable: list[CatalogCourse],
    placed_courses: set[str],
    excluded_ids: set[str],
    assigned_over_cap: bool,
) -> bool:
    if assigned_over_cap:
        return False
    return all(
        course.course_id in placed_courses or course.course_id in excluded_ids
        for course in placeable
    )


def _latest_map(repos: PlanningRepos, student_id: str) -> dict:
    record = repos.attempts.get_record(student_id)
    if record is None:
        return {}
    return {
        item.course_id: item
        for item in repos.attempts.latest_per_course(record.record_id)
    }


def _is_passed(attempt) -> bool:
    return (
        attempt is not None
        and attempt.result_status == "Passed"
        and attempt.grade is not None
    )


def _selection_reason(course: CatalogCourse, attempt) -> SelectionReason:
    if attempt is not None and attempt.result_status == "Failed":
        return SelectionReason.RETAKE_AFTER_FAIL
    if course.primary_status == CoursePrimaryStatus.ASSIGNED:
        return SelectionReason.ASSIGNED_THIS_SEMESTER
    if course.primary_status == CoursePrimaryStatus.BACKLOG:
        return SelectionReason.BACKLOG_FROM_SEMESTER_N
    if course.primary_status == CoursePrimaryStatus.RETAKE:
        return SelectionReason.RETAKE_IMPROVEMENT
    return SelectionReason.ELECTIVE_FILL


def generate_semester_plan(
    student_id: str,
    term_id: str,
    request: PlanRequest | None = None,
    *,
    repos: PlanningRepos,
) -> GeneratedPlan:
    request = request or PlanRequest()
    catalog = get_course_catalog(student_id, term_id, repos=repos)
    profile = repos.students.get_with_policy(student_id)
    term = repos.offerings.get_term(term_id)

    empty = GeneratedPlan(
        student_id=student_id,
        term_id=term_id,
        generation_mode=GenerationMode.FALLBACK,
        status=ToolStatus.UNCERTAIN,
        warnings=list(catalog.warnings),
    )
    if profile is None or profile.curriculum is None or term is None:
        if not empty.warnings:
            empty.warnings.append("Student, curriculum, or term was not found.")
        return empty
    if profile.program is None or profile.program.track is None:
        empty.warnings.append("Student has no program track, so credit limits are unknown.")
        return empty

    track = profile.program.track
    max_credits = track.max_credits_per_term
    min_credits = track.min_credits_per_term
    max_courses = track.max_courses
    min_courses = track.min_courses
    target = request.target_credit_load or profile.target_credit_load
    fill_goal = min(max(target, min_credits), max_credits)

    latest = _latest_map(repos, student_id)
    passed_ids = {
        course_id for course_id, attempt in latest.items() if _is_passed(attempt)
    }

    assigned = [
        course
        for course in catalog.courses
        if course.primary_status == CoursePrimaryStatus.ASSIGNED
    ]
    backlog = sorted(
        [
            course
            for course in catalog.courses
            if course.primary_status == CoursePrimaryStatus.BACKLOG
        ],
        key=lambda item: (item.assigned_semester, item.course_code),
    )
    unpassed_electives = [
        course
        for course in catalog.courses
        if not course.is_mandatory and course.course_id not in passed_ids
    ]
    unpassed_electives.sort(
        key=lambda item: (
            0 if is_offered_in(item.assigned_semester, term.term_type) else 1,
            -item.assigned_semester,
            item.course_code,
        )
    )
    retakes = sorted(
        [
            course
            for course in catalog.courses
            if course.primary_status == CoursePrimaryStatus.RETAKE
        ],
        key=lambda item: item.course_code,
    )

    items: list[PlanItem] = []
    exclusions: list[PlanExclusion] = []
    placed_sections: list[str] = []
    placed_courses: set[str] = set()
    warnings: list[str] = list(catalog.warnings)
    conflict_drop = False

    def total() -> int:
        return sum(item.credits for item in items)

    def count() -> int:
        return len(items)

    excluded_ids: set[str] = set()

    def exclude(course: CatalogCourse, reason: ExclusionReason) -> None:
        if course.course_id in excluded_ids or course.course_id in placed_courses:
            return
        excluded_ids.add(course.course_id)
        exclusions.append(
            PlanExclusion(
                course_id=course.course_id,
                course_code=course.course_code,
                reason=reason,
            )
        )

    def try_place(course: CatalogCourse, ignore_cap: bool) -> bool:
        nonlocal conflict_drop
        if course.course_id in placed_courses:
            return False
        if course.blocked:
            exclude(course, ExclusionReason.DROPPED_PREREQ_BLOCKED)
            return False
        if course.not_offered:
            exclude(course, ExclusionReason.DROPPED_NOT_OFFERED)
            return False
        if not ignore_cap:
            if count() >= max_courses or total() + course.credits > max_credits:
                exclude(course, ExclusionReason.DEFERRED_CREDIT_CAP)
                return False
        offering = repos.offerings.get_active_offering(course.course_id, term_id)
        if offering is None:
            exclude(course, ExclusionReason.DROPPED_NOT_OFFERED)
            return False
        sections = sorted(
            repos.offerings.list_sections_with_meetings(offering.offering_id),
            key=lambda section: section.section_code,
        )
        chosen = None
        for section in sections:
            clashes = detect_conflicts(
                placed_sections + [section.section_id],
                repos=repos,
            )
            if not clashes:
                chosen = section
                break
        if chosen is None:
            exclude(course, ExclusionReason.DROPPED_ALL_SECTIONS_CONFLICT)
            conflict_drop = True
            return False
        placed_sections.append(chosen.section_id)
        placed_courses.add(course.course_id)
        items.append(
            PlanItem(
                course_id=course.course_id,
                course_code=course.course_code,
                section_id=chosen.section_id,
                credits=course.credits,
                selection_reason=_selection_reason(
                    course, latest.get(course.course_id)
                ),
            )
        )
        return True

    for course in assigned:
        try_place(course, ignore_cap=True)

    placeable_electives: list[CatalogCourse] = []
    for course in unpassed_electives:
        if not is_offered_in(course.assigned_semester, term.term_type):
            continue
        if course.blocked:
            exclude(course, ExclusionReason.DROPPED_PREREQ_BLOCKED)
        elif course.not_offered:
            exclude(course, ExclusionReason.DROPPED_NOT_OFFERED)
        else:
            placeable_electives.append(course)

    assigned_over_cap = total() > max_credits
    if assigned_over_cap:
        warnings.append(_PORTAL_CAP_WARNING)
        for course in backlog:
            exclude(course, ExclusionReason.DEFERRED_CREDIT_CAP)
        rest = placeable_electives + (retakes if request.include_retakes else [])
        for course in rest:
            exclude(course, ExclusionReason.DEFERRED_CREDIT_CAP)
    else:
        for course in backlog:
            try_place(course, ignore_cap=False)

        elective_pool = list(placeable_electives)
        while elective_pool:
            if count() >= max_courses or total() >= max_credits:
                break
            if total() >= fill_goal and count() >= min_courses:
                break
            course = elective_pool.pop(0)
            if total() + course.credits > max_credits:
                exclude(course, ExclusionReason.DEFERRED_CREDIT_CAP)
                continue
            try_place(course, ignore_cap=False)

        if request.include_retakes:
            for course in retakes:
                if count() >= max_courses or total() >= max_credits:
                    break
                if total() + course.credits > max_credits:
                    exclude(course, ExclusionReason.DEFERRED_CREDIT_CAP)
                    continue
                try_place(course, ignore_cap=False)

    timetable: list[TimetableSlot] = []
    for item in items:
        for meeting in repos.offerings.get_meetings(item.section_id):
            timetable.append(
                TimetableSlot(
                    section_id=item.section_id,
                    course_code=item.course_code,
                    meeting_type=meeting.meeting_type,
                    day_of_week=meeting.day_of_week,
                    start_time=meeting.start_time,
                    end_time=meeting.end_time,
                    room=meeting.room,
                )
            )
    timetable.sort(key=lambda slot: (slot.day_of_week, slot.start_time.isoformat()))

    if conflict_drop:
        warnings.append("A timetable conflict forced a course to be dropped.")
    pool_exhausted = _pool_exhausted(
        placeable_electives, placed_courses, excluded_ids, assigned_over_cap
    )
    if pool_exhausted and total() < min_credits:
        warnings.append(
            f"Plan has {total()} credits {ELECTIVE_POOL_EXHAUSTED}; "
            f"minimum is {min_credits}."
        )
    if pool_exhausted and count() < min_courses:
        warnings.append(
            f"Plan has {count()} courses {ELECTIVE_POOL_EXHAUSTED}; "
            f"minimum is {min_courses}."
        )

    status = ToolStatus.OK
    if warnings or exclusions:
        status = ToolStatus.WARNING
    if catalog.status == ToolStatus.UNCERTAIN:
        status = ToolStatus.UNCERTAIN

    return GeneratedPlan(
        student_id=student_id,
        term_id=term_id,
        generation_mode=GenerationMode.FALLBACK,
        items=items,
        exclusions=exclusions,
        timetable=timetable,
        total_credits=total(),
        course_count=count(),
        status=status,
        warnings=list(dict.fromkeys(warnings)),
    )

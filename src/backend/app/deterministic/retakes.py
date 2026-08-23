"""Retake ranking (A-17).

A course is retakeable exactly when it is running this term (A-09b) and the
student still has an attempt left (`attempt_number` max 2). Ranking is not a
hard filter — ineligible rows stay in the list so A-18 can warn.
"""

from app.deterministic.cadence import is_offered_in
from app.deterministic.ports import PlanningRepos
from app.schemas.tools import RetakeCandidate


def rank_retakes(
    student_id: str,
    term_id: str,
    *,
    repos: PlanningRepos,
) -> list[RetakeCandidate]:
    profile = repos.students.get_with_policy(student_id)
    term = repos.offerings.get_term(term_id)
    if profile is None or profile.curriculum_id is None or term is None:
        return []

    record = repos.attempts.get_record(student_id)
    if record is None:
        return []

    latest = repos.attempts.latest_per_course(record.record_id)
    if not latest:
        return []

    curr_rows = {
        course.course_id: row
        for row, course in repos.curriculum.list_courses_for_student(
            profile.curriculum_id, profile.spec_code
        )
    }

    candidates: list[RetakeCandidate] = []
    for attempt in latest:
        course = repos.courses.get_by_id(attempt.course_id)
        if course is None:
            continue
        row = curr_rows.get(attempt.course_id)
        if row is None:
            continue
        offering = repos.offerings.get_active_offering(course.course_id, term_id)
        offered = offering is not None and is_offered_in(
            row.assigned_semester, term.term_type
        )
        attempt_count = attempt.attempt_number
        eligible = offered and attempt_count < 2
        grade = float(attempt.grade) if attempt.grade is not None else None
        candidates.append(
            RetakeCandidate(
                course_id=course.course_id,
                course_code=course.course_code,
                last_grade=grade,
                last_result_status=attempt.result_status,
                attempt_count=attempt_count,
                eligible=eligible,
                offered_this_term=offered,
            )
        )

    def sort_key(item: RetakeCandidate) -> tuple:
        failed = 0 if item.last_result_status == "Failed" else 1
        grade_key = item.last_grade if item.last_grade is not None else 99.0
        return (failed, grade_key, item.course_code)

    candidates.sort(key=sort_key)
    return candidates

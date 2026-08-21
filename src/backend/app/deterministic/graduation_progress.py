from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CompletedCourse:
    course_code: str
    credits: int


@dataclass(frozen=True)
class GraduationCalculation:
    earned_credits: int
    required_credits: int

    remaining_credits: int

    credit_requirement_met: bool

    completed_required_courses: list[str]
    missing_required_courses: list[str]

    completed: bool

    progress_percentage: float


def calculate_graduation_progress(
    completed_courses: Iterable[CompletedCourse],
    required_credits: int,
    required_course_codes: Iterable[str],
) -> GraduationCalculation:

    completed_list = list(completed_courses)

    credits_by_course: dict[str, int] = {}

    for course in completed_list:
        credits_by_course[course.course_code] = course.credits

    earned_credits = sum(
        credits_by_course.values()
    )

    required_codes = sorted(
        set(required_course_codes)
    )

    completed_codes = set(
        credits_by_course
    )

    completed_required_courses = [
        code
        for code in required_codes
        if code in completed_codes
    ]

    missing_required_courses = [
        code
        for code in required_codes
        if code not in completed_codes
    ]

    remaining_credits = max(
        required_credits - earned_credits,
        0,
    )

    credit_requirement_met = (
        earned_credits >= required_credits
    )

    completed = (
        credit_requirement_met
        and len(missing_required_courses) == 0
    )

    if required_credits <= 0:
        progress_percentage = 100.0

    else:
        progress_percentage = min(
            round(
                (
                    earned_credits
                    / required_credits
                )
                * 100,
                2,
            ),
            100.0,
        )

    return GraduationCalculation(
        earned_credits=earned_credits,

        required_credits=required_credits,

        remaining_credits=remaining_credits,

        credit_requirement_met=credit_requirement_met,

        completed_required_courses=(
            completed_required_courses
        ),

        missing_required_courses=(
            missing_required_courses
        ),

        completed=completed,

        progress_percentage=progress_percentage,
    )
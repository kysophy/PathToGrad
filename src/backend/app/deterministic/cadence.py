"""Programme semester vs calendar term — keep the two questions apart.

A calendar term such as 2026.1 has no programme-semester number. What it has
is a yearly slot (`TermType`: Semester1 / Semester2 / Summer). A course runs
in the slot of its `assigned_semester`:

    1, 4, 7 → Semester1
    2, 5, 8 → Semester2
    3, 6, 9 → Summer

Whether a course is Assigned or Backlog for *this student* is a different
comparison (`assigned_semester` vs `student.current_semester`). Do not mix
them. Retake eligibility is “is it offered this term?”, not a second formula.
"""

from app.deterministic.types import TermType

_SLOT = {
    1: TermType.SEMESTER_1,
    2: TermType.SEMESTER_2,
    0: TermType.SUMMER,
}


class CadenceMismatchError(ValueError):
    """An offering row sits in the wrong yearly slot for its assigned semester."""


def coerce_term_type(term_type: TermType | str) -> TermType:
    if isinstance(term_type, TermType):
        return term_type
    return TermType(term_type)


def position_of(semester_no: int) -> TermType:
    """Programme semester -> the yearly slot the course runs in."""
    return _SLOT[semester_no % 3]


def is_offered_in(semester_no: int, term_type: TermType | str) -> bool:
    return position_of(semester_no) == coerce_term_type(term_type)


def assert_offered_in(
    semester_no: int,
    term_type: TermType | str,
    *,
    course_code: str = "",
) -> None:
    """Raise if this course's assigned semester does not match the term's slot."""
    slot = coerce_term_type(term_type)
    if is_offered_in(semester_no, slot):
        return
    where = f" for {course_code}" if course_code else ""
    raise CadenceMismatchError(
        f"Course{where} is assigned to semester {semester_no} "
        f"({position_of(semester_no).value}), which does not run in a "
        f"{slot.value} term."
    )

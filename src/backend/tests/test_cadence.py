import pytest

from app.deterministic.cadence import (
    CadenceMismatchError,
    assert_offered_in,
    is_offered_in,
    position_of,
)
from app.deterministic.types import TermType

# semester_no % 3 → yearly slot. Cover 1–9 against all three TermTypes.
_EXPECTED = {
    1: TermType.SEMESTER_1,
    2: TermType.SEMESTER_2,
    3: TermType.SUMMER,
    4: TermType.SEMESTER_1,
    5: TermType.SEMESTER_2,
    6: TermType.SUMMER,
    7: TermType.SEMESTER_1,
    8: TermType.SEMESTER_2,
    9: TermType.SUMMER,
}


@pytest.mark.parametrize("semester_no,slot", list(_EXPECTED.items()))
def test_position_of_semesters_1_to_9(semester_no: int, slot: TermType):
    assert position_of(semester_no) is slot


@pytest.mark.parametrize("semester_no,slot", list(_EXPECTED.items()))
@pytest.mark.parametrize("other", list(TermType))
def test_is_offered_in_matches_only_own_slot(
    semester_no: int,
    slot: TermType,
    other: TermType,
):
    assert is_offered_in(semester_no, other) is (other is slot)


def test_is_offered_in_accepts_string_term_type():
    assert is_offered_in(2, "Semester2") is True
    assert is_offered_in(2, "Semester1") is False


def test_assert_offered_in_accepts_matching_slot():
    assert_offered_in(8, TermType.SEMESTER_2, course_code="CSC13010")


def test_importer_refuses_wrong_slot():
    with pytest.raises(CadenceMismatchError, match="CSC99999"):
        assert_offered_in(1, TermType.SEMESTER_2, course_code="CSC99999")


def test_demo_term_semester2_accepts_2_5_8():
    for semester_no in (2, 5, 8):
        assert is_offered_in(semester_no, TermType.SEMESTER_2)
    for semester_no in (1, 3, 4, 6, 7, 9):
        assert not is_offered_in(semester_no, TermType.SEMESTER_2)


def test_offerings_csv_matches_semester2_slots():
    """Prove the real CSV (not just the helper) matches C-01. No MySQL."""
    import csv
    from pathlib import Path

    data = Path(__file__).resolve().parents[3] / "data"
    assigned: dict[str, int] = {}
    with (data / "Courses.csv").open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["spec_code"] not in {"GEN", "SE"}:
                continue
            code = row["course_code"]
            semester_no = int(row["semester_no"])
            previous = assigned.get(code)
            if previous is None or semester_no < previous:
                assigned[code] = semester_no

    with (data / "offerings.csv").open(encoding="utf-8-sig", newline="") as fh:
        codes = {row["course_code"].strip() for row in csv.DictReader(fh)}

    for code in sorted(codes):
        assert code in assigned, f"{code} is offered but has no GEN+SE curriculum row"
        assert is_offered_in(assigned[code], TermType.SEMESTER_2), (
            f"{code} is assigned to semester {assigned[code]}, "
            "which does not run in a Semester2 term"
        )

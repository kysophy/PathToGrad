"""A-13 — write these cases first; the implementation must satisfy them."""

from tests.fakes import FakeAttempt, FakeCourse, FakeCurrRow, build_repos

from app.deterministic.progress import get_graduation_progress
from app.deterministic.types import ToolStatus


def _repos(attempts, spec_code="SE", required_credits=20):
    courses = [
        FakeCourse("c1", "CSC10012", credits=4),
        FakeCourse("c2", "CSC10004", credits=4),
        FakeCourse("c3", "BAA00021", credits=3),
        FakeCourse("c4", "CSC10003", credits=4),
    ]
    rows = [
        FakeCurrRow("c1", 1, "Core", "GEN"),
        FakeCurrRow("c2", 2, "Core", "GEN"),
        FakeCurrRow("c4", 3, "Core", "GEN"),
        FakeCurrRow("c3", 2, "Elective", "GEN"),
    ]
    return build_repos(
        current_semester=5,
        spec_code=spec_code,
        courses=courses,
        curr_rows=rows,
        attempts=attempts,
        required_credits=required_credits,
    )


def test_only_passed_attempts_count():
    repos = _repos(
        [
            FakeAttempt("c1", 1, "Passed", grade=8.0, credits_earned=4),
            FakeAttempt("c2", 1, "Failed", grade=4.0, credits_earned=0),
            FakeAttempt("c3", 1, "InProgress", grade=None, credits_earned=0),
        ]
    )
    result = get_graduation_progress("S1", repos=repos)
    assert result.earned_credits == 4
    assert result.mandatory_passed is False
    assert "CSC10004" in result.missing_required_courses
    assert "CSC10003" in result.missing_required_courses


def test_credits_met_without_mandatory_is_not_complete():
    # TC-14: credits alone are not enough
    repos = _repos(
        [
            FakeAttempt("c1", 1, "Passed", grade=8.0),
            FakeAttempt("c2", 1, "Passed", grade=8.0),
            FakeAttempt("c3", 1, "Passed", grade=8.0),
            FakeAttempt("c4", 1, "Failed", grade=4.0),
        ],
        required_credits=11,
    )
    result = get_graduation_progress("S1", repos=repos)
    assert result.credit_requirement_met is True
    assert result.mandatory_passed is False
    assert result.completed is False
    assert result.missing_required_courses == ["CSC10003"]


def test_gpa_uses_latest_attempt_not_best():
    repos = _repos(
        [
            FakeAttempt("c1", 1, "Passed", grade=9.0),
            FakeAttempt("c1", 2, "Passed", grade=5.0),
            FakeAttempt("c2", 1, "Passed", grade=7.0),
            FakeAttempt("c4", 1, "Passed", grade=8.0),
        ],
        required_credits=12,
    )
    result = get_graduation_progress("S1", repos=repos)
    # latest grades 5, 7, 8 on 4-credit courses → 20/12
    assert result.gpa == 6.67
    assert result.earned_credits == 12
    assert result.mandatory_passed is True
    assert result.completed is True


def test_passed_without_grade_is_uncertain_and_uncounted():
    repos = _repos([FakeAttempt("c1", 1, "Passed", grade=None)])
    result = get_graduation_progress("S1", repos=repos)
    assert result.status == ToolStatus.UNCERTAIN
    assert result.earned_credits == 0
    assert result.warnings


def test_gpa_is_credit_weighted_and_skips_inprogress():
    courses = [
        FakeCourse("c1", "CSC10012", credits=4),
        FakeCourse("c2", "CSC10004", credits=2),
        FakeCourse("c3", "BAA00021", credits=3),
        FakeCourse("c4", "CSC10003", credits=4),
    ]
    rows = [
        FakeCurrRow("c1", 1, "Core", "GEN"),
        FakeCurrRow("c2", 2, "Core", "GEN"),
        FakeCurrRow("c4", 3, "Core", "GEN"),
        FakeCurrRow("c3", 2, "Elective", "GEN"),
    ]
    repos = build_repos(
        current_semester=5,
        spec_code="SE",
        courses=courses,
        curr_rows=rows,
        attempts=[
            FakeAttempt("c1", 1, "Passed", grade=10.0),
            FakeAttempt("c2", 1, "Failed", grade=4.0),
            FakeAttempt("c3", 1, "InProgress", grade=9.0),
        ],
        required_credits=20,
    )
    result = get_graduation_progress("S1", repos=repos)
    # InProgress 9.0 must not count. (10*4 + 4*2) / 6 = 8.0
    assert result.gpa == 8.0
    assert result.earned_credits == 4

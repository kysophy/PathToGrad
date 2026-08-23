from tests.fakes import (
    FakeAttempt,
    FakeCourse,
    FakeCurrRow,
    build_repos,
    offering_with,
    section_with,
    meeting,
)

from app.deterministic.retakes import rank_retakes


TERM = "TERM-2026-1"


def _repos(attempts, offerings=None, current_semester=5):
    courses = [
        FakeCourse("c1", "CSC10012", credits=4),
        FakeCourse("c2", "CSC10004", credits=4),
        FakeCourse("c3", "CSC10003", credits=4),
    ]
    rows = [
        FakeCurrRow("c1", 2, "Core"),
        FakeCurrRow("c2", 2, "Core"),
        FakeCurrRow("c3", 3, "Core"),
    ]
    if offerings is None:
        offerings = [
            offering_with(
                "off-1",
                "c1",
                TERM,
                section_with("s1", "off-1", "01", meeting("Monday", "07:30", "11:10")),
            ),
            offering_with(
                "off-2",
                "c2",
                TERM,
                section_with("s2", "off-2", "01", meeting("Tuesday", "07:30", "11:10")),
            ),
        ]
    return build_repos(
        current_semester=current_semester,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        attempts=attempts,
        offerings=offerings,
    )


def test_offered_failed_course_is_eligible():
    repos = _repos([FakeAttempt("c1", 1, "Failed", grade=4.0)])
    ranked = rank_retakes("S1", TERM, repos=repos)
    by_code = {item.course_code: item for item in ranked}
    assert by_code["CSC10012"].eligible is True
    assert by_code["CSC10012"].offered_this_term is True
    assert by_code["CSC10012"].attempt_count == 1


def test_third_attempt_is_not_eligible():
    repos = _repos([FakeAttempt("c1", 2, "Failed", grade=3.0)])
    ranked = rank_retakes("S1", TERM, repos=repos)
    assert ranked[0].eligible is False
    assert ranked[0].attempt_count == 2


def test_wrong_slot_is_not_offered_this_term():
    # c3 is semester 3 (Summer); demo term is Semester2
    repos = _repos([FakeAttempt("c3", 1, "Failed", grade=4.0)], offerings=[])
    ranked = rank_retakes("S1", TERM, repos=repos)
    assert ranked[0].course_code == "CSC10003"
    assert ranked[0].offered_this_term is False
    assert ranked[0].eligible is False


def test_failed_ranks_before_passed_improvement():
    repos = _repos(
        [
            FakeAttempt("c1", 1, "Passed", grade=6.0),
            FakeAttempt("c2", 1, "Failed", grade=4.0),
        ]
    )
    ranked = rank_retakes("S1", TERM, repos=repos)
    assert [item.course_code for item in ranked] == ["CSC10004", "CSC10012"]

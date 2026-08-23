"""A-11 / A-12 — write these cases first; the implementation must satisfy them."""

from tests.fakes import (
    FakeAttempt,
    FakeCourse,
    FakeCurrRow,
    FakePrereq,
    build_repos,
)

from app.deterministic.prerequisites import (
    check_prerequisites,
    find_prerequisite_cycles,
)
from app.deterministic.types import ToolStatus


def _base_courses():
    return [
        FakeCourse("c-base", "CSC10012", name_en="Programming Fundamentals"),
        FakeCourse("c-dep", "CSC10004", name_en="Data Structures"),
        FakeCourse("c-oop", "CSC10003", name_en="Object-Oriented Programming"),
    ]


def _curr_rows():
    return [
        FakeCurrRow("c-base", 1, "Core"),
        FakeCurrRow("c-dep", 2, "Core"),
        FakeCurrRow("c-oop", 3, "Core"),
    ]


def test_no_prerequisites_is_satisfied():
    # TC-16
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=_base_courses(),
        curr_rows=_curr_rows(),
    )
    results = check_prerequisites("S1", ["c-base"], repos=repos)
    assert len(results) == 1
    assert results[0].satisfied is True
    assert results[0].status == ToolStatus.OK
    assert results[0].prerequisites == []
    assert results[0].missing == []


def test_all_prerequisites_passed_is_satisfied():
    # TC-17
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=_base_courses(),
        curr_rows=_curr_rows(),
        prereqs=[FakePrereq("c-dep", "c-base")],
        attempts=[
            FakeAttempt("c-base", 1, "Passed", grade=8.0),
        ],
    )
    results = check_prerequisites("S1", ["c-dep"], repos=repos)
    assert results[0].satisfied is True
    assert results[0].status == ToolStatus.OK
    assert results[0].missing == []
    assert results[0].prerequisites[0].course_code == "CSC10012"
    assert results[0].prerequisites[0].satisfied is True
    assert results[0].prerequisites[0].attempt_status == "Passed"


def test_failed_inprogress_and_missing_are_named():
    # TC-18 — three distinct unmet reasons
    repos = build_repos(
        current_semester=3,
        spec_code=None,
        courses=_base_courses(),
        curr_rows=_curr_rows(),
        prereqs=[
            FakePrereq("c-oop", "c-base"),
            FakePrereq("c-oop", "c-dep"),
        ],
        attempts=[
            FakeAttempt("c-base", 1, "Failed", grade=4.0),
            FakeAttempt("c-dep", 1, "InProgress", grade=None),
        ],
    )
    # also check a course whose prereq has no attempt at all by adding a third required
    courses = _base_courses() + [
        FakeCourse("c-db", "CSC10006", name_en="Databases"),
    ]
    rows = _curr_rows() + [FakeCurrRow("c-db", 4, "Core")]
    repos = build_repos(
        current_semester=4,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        prereqs=[
            FakePrereq("c-oop", "c-base"),
            FakePrereq("c-db", "c-dep"),
            FakePrereq("c-db", "c-oop"),
        ],
        attempts=[
            FakeAttempt("c-base", 1, "Failed", grade=4.0),
            FakeAttempt("c-dep", 1, "InProgress", grade=None),
        ],
    )
    failed = check_prerequisites("S1", ["c-oop"], repos=repos)[0]
    assert failed.satisfied is False
    assert failed.missing[0].course_code == "CSC10012"
    assert failed.missing[0].attempt_status == "Failed"

    mixed = check_prerequisites("S1", ["c-db"], repos=repos)[0]
    assert mixed.satisfied is False
    statuses = {item.course_code: item.attempt_status for item in mixed.missing}
    assert statuses["CSC10004"] == "InProgress"
    assert statuses["CSC10003"] == "Missing"


def test_incomplete_pass_is_uncertain_with_warning():
    # TC-19 — never a silent eligible
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=_base_courses(),
        curr_rows=_curr_rows(),
        prereqs=[FakePrereq("c-dep", "c-base")],
        attempts=[
            FakeAttempt("c-base", 1, "Passed", grade=None),
        ],
    )
    result = check_prerequisites("S1", ["c-dep"], repos=repos)[0]
    assert result.satisfied is None
    assert result.status == ToolStatus.UNCERTAIN
    assert result.warnings
    assert result.prerequisites[0].satisfied is None
    assert result.prerequisites[0].warning is not None


def test_cycle_is_reported_and_does_not_hang():
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=_base_courses(),
        curr_rows=_curr_rows(),
        prereqs=[
            FakePrereq("c-base", "c-dep"),
            FakePrereq("c-dep", "c-base"),
        ],
    )
    results = check_prerequisites("S1", ["c-base", "c-dep"], repos=repos)
    assert len(results) == 2
    assert any(item.status == ToolStatus.UNCERTAIN for item in results)
    assert any("cycle" in warning.lower() for item in results for warning in item.warnings)


def test_find_prerequisite_cycles_returns_the_loop():
    cycles = find_prerequisite_cycles(
        edges=[("A", "B"), ("B", "C"), ("C", "A")],
    )
    assert len(cycles) == 1
    loop = cycles[0]
    assert loop[0] == loop[-1]
    assert set(loop[:-1]) == {"A", "B", "C"}


def test_find_prerequisite_cycles_empty_when_dag():
    assert find_prerequisite_cycles(edges=[("B", "A"), ("C", "B")]) == []


def test_find_prerequisite_cycles_filters_course_ids():
    cycles = find_prerequisite_cycles(
        course_ids=["X", "Y"],
        edges=[("A", "B"), ("B", "A"), ("X", "Y"), ("Y", "X")],
    )
    assert len(cycles) == 1
    assert set(cycles[0][:-1]) == {"X", "Y"}


def test_cycle_is_visible_when_only_one_end_is_requested():
    cycles = find_prerequisite_cycles(
        course_ids=["A"],
        edges=[("A", "B"), ("B", "A")],
    )
    assert len(cycles) == 1
    assert set(cycles[0][:-1]) == {"A", "B"}


def test_latest_failed_retake_unsatisfies_even_if_earlier_pass():
    repos = build_repos(
        current_semester=5,
        spec_code=None,
        courses=_base_courses(),
        curr_rows=_curr_rows(),
        prereqs=[FakePrereq("c-dep", "c-base")],
        attempts=[
            FakeAttempt("c-base", 1, "Passed", grade=8.0),
            FakeAttempt("c-base", 2, "Failed", grade=4.0),
        ],
    )
    result = check_prerequisites("S1", ["c-dep"], repos=repos)[0]
    assert result.satisfied is False
    assert result.missing[0].attempt_status == "Failed"


def test_missing_student_is_uncertain():
    repos = build_repos(
        current_semester=1,
        spec_code=None,
        courses=_base_courses(),
        curr_rows=_curr_rows(),
    )
    results = check_prerequisites("NO-SUCH", ["c-base"], repos=repos)
    assert results[0].status == ToolStatus.UNCERTAIN
    assert results[0].satisfied is None

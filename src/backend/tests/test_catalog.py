from tests.fakes import (
    FakeAttempt,
    FakeCourse,
    FakeCurrRow,
    FakePrereq,
    build_repos,
    meeting,
    offering_with,
    section_with,
)

from app.deterministic.catalog import get_course_catalog
from app.deterministic.types import CoursePrimaryStatus, ToolStatus
from app.schemas.tools import CatalogFilters

TERM = "TERM-2026-1"


def _world(**kwargs):
    courses = [
        FakeCourse("c-s1", "CSC10012", credits=4),
        FakeCourse("c-s2", "CSC10004", credits=4),
        FakeCourse("c-s5", "CSC10006", credits=4),
        FakeCourse("c-el", "BAA00021", credits=3),
        FakeCourse("c-fut", "CSC13002", credits=4),
        FakeCourse("c-miss", "CSC13001", credits=4),
        FakeCourse("c-se", "CSC13010", credits=4),
    ]
    rows = [
        FakeCurrRow("c-s1", 1, "Core", "GEN"),
        FakeCurrRow("c-s2", 2, "Core", "GEN"),
        FakeCurrRow("c-s5", 5, "Core", "GEN"),
        FakeCurrRow("c-el", 2, "Elective", "GEN"),
        FakeCurrRow("c-fut", 7, "Core", "SE"),
        FakeCurrRow("c-miss", 8, "Core", "SE"),
        FakeCurrRow("c-se", 8, "Core", "SE"),
    ]
    offerings = [
        offering_with(
            "off-s2",
            "c-s2",
            TERM,
            section_with("sec-s2", "off-s2", "01", meeting("Monday", "07:30", "11:10")),
        ),
        offering_with(
            "off-s5",
            "c-s5",
            TERM,
            section_with("sec-s5", "off-s5", "01", meeting("Tuesday", "07:30", "11:10")),
        ),
        offering_with(
            "off-el",
            "c-el",
            TERM,
            section_with("sec-el", "off-el", "01", meeting("Wednesday", "13:30", "15:30", "TH")),
        ),
        offering_with(
            "off-se",
            "c-se",
            TERM,
            section_with("sec-se", "off-se", "01", meeting("Friday", "07:30", "11:10")),
        ),
    ]
    return build_repos(
        courses=courses,
        curr_rows=rows,
        offerings=offerings,
        prereqs=[FakePrereq("c-s5", "c-s2")],
        **kwargs,
    )


def _by_code(result):
    return {item.course_code: item for item in result.courses}


def test_assigned_backlog_elective_future_and_not_offered():
    repos = _world(current_semester=5, spec_code="SE")
    result = get_course_catalog("S1", TERM, repos=repos)
    assert result.status in {ToolStatus.OK, ToolStatus.WARNING}
    by_code = _by_code(result)
    assert by_code["CSC10006"].primary_status == CoursePrimaryStatus.ASSIGNED
    assert by_code["CSC10004"].primary_status == CoursePrimaryStatus.BACKLOG
    assert by_code["CSC10012"].primary_status == CoursePrimaryStatus.BACKLOG
    assert by_code["BAA00021"].primary_status == CoursePrimaryStatus.ELECTIVE
    assert by_code["CSC13002"].primary_status == CoursePrimaryStatus.FUTURE
    assert by_code["CSC13001"].not_offered is True
    assert by_code["CSC13010"].not_offered is False
    # semester-1 course does not run in a Semester2 term
    assert by_code["CSC10012"].not_offered is True
    assert by_code["CSC10004"].not_offered is False


def test_blocked_overlay_when_prereq_unmet():
    repos = _world(current_semester=5, spec_code="SE")
    by_code = _by_code(get_course_catalog("S1", TERM, repos=repos))
    assert by_code["CSC10006"].blocked is True


def test_retake_when_passed_and_offered():
    repos = _world(
        current_semester=5,
        spec_code="SE",
        attempts=[FakeAttempt("c-s2", 1, "Passed", grade=7.0)],
    )
    by_code = _by_code(get_course_catalog("S1", TERM, repos=repos))
    assert by_code["CSC10004"].primary_status == CoursePrimaryStatus.RETAKE
    assert by_code["CSC10006"].blocked is False


def test_no_spec_hides_se_rows():
    repos = _world(current_semester=2, spec_code=None)
    result = get_course_catalog("S1", TERM, repos=repos)
    codes = {item.course_code for item in result.courses}
    assert "CSC13010" not in codes
    assert "CSC10004" in codes
    by_code = _by_code(result)
    assert by_code["CSC10004"].primary_status == CoursePrimaryStatus.ASSIGNED


def test_filters_offered_only_and_primary_status():
    repos = _world(current_semester=5, spec_code="SE")
    filtered = get_course_catalog(
        "S1",
        TERM,
        CatalogFilters(primary_status=CoursePrimaryStatus.ASSIGNED, offered_only=True),
        repos=repos,
    )
    assert [item.course_code for item in filtered.courses] == ["CSC10006"]

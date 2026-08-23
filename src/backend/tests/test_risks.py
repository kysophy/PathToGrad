from tests.fakes import (
    FakeAttempt,
    FakeCourse,
    FakeCurrRow,
    FakePrereq,
    FakeTrack,
    build_repos,
    meeting,
    offering_with,
    section_with,
)

from app.deterministic.generator import generate_semester_plan
from app.deterministic.risks import detect_risks
from app.deterministic.types import RiskCode, SelectionReason
from app.schemas.enums import GenerationMode
from app.schemas.tools import GeneratedPlan, PlanItem

TERM = "TERM-2026-1"


def test_no_retake_remaining_and_gpa_and_stale_backlog():
    courses = [
        FakeCourse("c1", "CSC10012", credits=4),
        FakeCourse("c2", "CSC10004", credits=4),
    ]
    rows = [
        FakeCurrRow("c1", 1, "Core"),
        FakeCurrRow("c2", 2, "Core"),
    ]
    repos = build_repos(
        current_semester=8,
        spec_code="SE",
        courses=courses,
        curr_rows=rows,
        attempts=[
            FakeAttempt("c1", 2, "Failed", grade=3.0),
            FakeAttempt("c2", 1, "Passed", grade=4.0),
        ],
        required_credits=138,
    )
    codes = {item.code for item in detect_risks("S1", repos=repos, term_id=TERM)}
    assert RiskCode.NO_RETAKE_REMAINING in codes
    assert RiskCode.GPA_BELOW_THRESHOLD in codes
    assert RiskCode.BACKLOG_STALE in codes


def test_specialization_not_set_from_semester_7():
    repos = build_repos(
        current_semester=7,
        spec_code=None,
        courses=[FakeCourse("c1", "CSC10012", credits=4)],
        curr_rows=[FakeCurrRow("c1", 1, "Core")],
    )
    codes = {item.code for item in detect_risks("S1", repos=repos)}
    assert RiskCode.SPECIALIZATION_NOT_SET in codes


def test_retake_replaces_grade_on_plan():
    plan = GeneratedPlan(
        student_id="S1",
        term_id=TERM,
        generation_mode=GenerationMode.FALLBACK,
        items=[
            PlanItem(
                course_id="c1",
                course_code="CSC10004",
                section_id="s1",
                credits=4,
                selection_reason=SelectionReason.RETAKE_IMPROVEMENT,
            )
        ],
        total_credits=4,
        course_count=1,
    )
    repos = build_repos(
        current_semester=5,
        spec_code="SE",
        courses=[FakeCourse("c1", "CSC10004", credits=4)],
        curr_rows=[FakeCurrRow("c1", 2, "Core")],
        attempts=[FakeAttempt("c1", 1, "Passed", grade=6.0)],
        track=FakeTrack(
            track_id="TRACK-STD-001",
            min_credits_per_term=4,
            min_courses=1,
        ),
    )
    codes = {item.code for item in detect_risks("S1", plan, repos=repos, term_id=TERM)}
    assert RiskCode.RETAKE_REPLACES_GRADE in codes


def test_prereq_blocked_risk_for_assigned_course():
    courses = [
        FakeCourse("need", "CSC10006", credits=4),
        FakeCourse("base", "CSC10004", credits=4),
    ]
    rows = [
        FakeCurrRow("need", 5, "Core"),
        FakeCurrRow("base", 2, "Core"),
    ]
    offerings = [
        offering_with(
            "off-need",
            "need",
            TERM,
            section_with(
                "s-need",
                "off-need",
                "01",
                meeting("Monday", "07:30", "11:10"),
            ),
        )
    ]
    repos = build_repos(
        current_semester=5,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        prereqs=[FakePrereq("need", "base")],
        offerings=offerings,
    )
    codes = {item.code for item in detect_risks("S1", repos=repos, term_id=TERM)}
    assert RiskCode.PREREQ_BLOCKED in codes


def test_plan_under_min_emits_load_risks():
    plan = generate_semester_plan(
        "S1",
        TERM,
        repos=build_repos(
            current_semester=8,
            spec_code="SE",
            courses=[FakeCourse("a1", "CSC13001", credits=4)],
            curr_rows=[FakeCurrRow("a1", 8, "Core", "SE")],
            offerings=[],
        ),
    )
    repos = build_repos(
        current_semester=8,
        spec_code="SE",
        courses=[FakeCourse("a1", "CSC13001", credits=4)],
        curr_rows=[FakeCurrRow("a1", 8, "Core", "SE")],
        offerings=[],
    )
    codes = {item.code for item in detect_risks("S1", plan, repos=repos, term_id=TERM)}
    assert RiskCode.LOAD_UNDER_MIN in codes
    assert RiskCode.COURSE_COUNT_UNDER_MIN in codes
    assert RiskCode.COURSE_NOT_OFFERED in codes

"""A-16 — write these cases first; the implementation must satisfy them."""

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
from app.deterministic.types import ExclusionReason, SelectionReason
from app.schemas.tools import PlanRequest

TERM = "TERM-2026-1"


def _offering(course_id: str, section_id: str, day: str, start: str, end: str, kind="LT"):
    return offering_with(
        f"off-{course_id}",
        course_id,
        TERM,
        section_with(
            section_id,
            f"off-{course_id}",
            "01",
            meeting(day, start, end, kind),
        ),
    )


def test_elective_soft_lock_fills_to_min_credits_and_min_courses():
    courses = [
        FakeCourse("a1", "CSC10004", credits=4),
        FakeCourse("a2", "CSC10009", credits=4),
        FakeCourse("e1", "BAA00021", credits=3),
        FakeCourse("e2", "BAA00022", credits=3),
        FakeCourse("e3", "PHY00001", credits=3),
    ]
    rows = [
        FakeCurrRow("a1", 2, "Core"),
        FakeCurrRow("a2", 2, "Core"),
        FakeCurrRow("e1", 2, "Elective"),
        FakeCurrRow("e2", 2, "Elective"),
        FakeCurrRow("e3", 5, "Elective"),
    ]
    offerings = [
        _offering("a1", "s-a1", "Monday", "07:30", "11:10"),
        _offering("a2", "s-a2", "Tuesday", "07:30", "11:10"),
        _offering("e1", "s-e1", "Wednesday", "07:30", "09:30", "TH"),
        _offering("e2", "s-e2", "Thursday", "07:30", "09:30", "TH"),
        _offering("e3", "s-e3", "Friday", "07:30", "09:30", "TH"),
    ]
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        target_credit_load=18,
        courses=courses,
        curr_rows=rows,
        offerings=offerings,
    )
    plan = generate_semester_plan("S1", TERM, PlanRequest(), repos=repos)
    assert plan.total_credits >= 14
    assert plan.course_count >= 4
    reasons = {item.course_code: item.selection_reason for item in plan.items}
    assert reasons["CSC10004"] == SelectionReason.ASSIGNED_THIS_SEMESTER
    assert SelectionReason.ELECTIVE_FILL in reasons.values()
    assert len({item.course_id for item in plan.items}) == len(plan.items)


def test_assigned_over_cap_keeps_assigned_and_defers_backlog():
    track = FakeTrack(
        track_id="TRACK-STD-001",
        max_credits_per_term=7,
        min_credits_per_term=4,
        min_courses=1,
    )
    courses = [
        FakeCourse("a1", "CSC10006", credits=4),
        FakeCourse("a2", "CSC10009", credits=4),
        FakeCourse("b1", "CSC10004", credits=4),
    ]
    rows = [
        FakeCurrRow("a1", 5, "Core"),
        FakeCurrRow("a2", 5, "Core"),
        FakeCurrRow("b1", 2, "Core"),
    ]
    offerings = [
        _offering("a1", "s-a1", "Monday", "07:30", "11:10"),
        _offering("a2", "s-a2", "Tuesday", "07:30", "11:10"),
        _offering("b1", "s-b1", "Wednesday", "07:30", "11:10"),
    ]
    repos = build_repos(
        current_semester=5,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        offerings=offerings,
        track=track,
    )
    plan = generate_semester_plan("S1", TERM, repos=repos)
    codes = {item.course_code for item in plan.items}
    assert codes == {"CSC10006", "CSC10009"}
    assert any(
        item.course_code == "CSC10004"
        and item.reason == ExclusionReason.DEFERRED_CREDIT_CAP
        for item in plan.exclusions
    )
    assert any("Maximum credits reached" in text for text in plan.warnings)


def test_all_sections_conflict_drops_with_reason():
    courses = [
        FakeCourse("a1", "CSC10004", credits=4),
        FakeCourse("a2", "CSC10009", credits=4),
    ]
    rows = [
        FakeCurrRow("a1", 2, "Core"),
        FakeCurrRow("a2", 2, "Core"),
    ]
    offerings = [
        _offering("a1", "s-a1", "Monday", "07:30", "11:10"),
        _offering("a2", "s-a2", "Monday", "09:30", "11:30", "TH"),
    ]
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        target_credit_load=8,
        courses=courses,
        curr_rows=rows,
        offerings=offerings,
        track=FakeTrack(
            track_id="TRACK-STD-001",
            min_credits_per_term=4,
            max_credits_per_term=24,
            min_courses=1,
            max_courses=6,
        ),
    )
    plan = generate_semester_plan("S1", TERM, repos=repos)
    assert any(
        item.reason == ExclusionReason.DROPPED_ALL_SECTIONS_CONFLICT
        for item in plan.exclusions
    )
    assert plan.course_count == 1


def test_missing_offering_is_dropped_not_invented():
    courses = [FakeCourse("a1", "CSC13001", credits=4)]
    rows = [FakeCurrRow("a1", 8, "Core", "SE")]
    repos = build_repos(
        current_semester=8,
        spec_code="SE",
        courses=courses,
        curr_rows=rows,
        offerings=[],
        track=FakeTrack(
            track_id="TRACK-STD-001",
            min_credits_per_term=4,
            min_courses=1,
        ),
    )
    plan = generate_semester_plan("S1", TERM, repos=repos)
    assert plan.items == []
    assert plan.exclusions[0].reason == ExclusionReason.DROPPED_NOT_OFFERED
    assert plan.exclusions[0].course_code == "CSC13001"


def test_prereq_blocked_is_excluded():
    courses = [
        FakeCourse("need", "CSC10006", credits=4),
        FakeCourse("base", "CSC10004", credits=4),
    ]
    rows = [
        FakeCurrRow("need", 5, "Core"),
        FakeCurrRow("base", 2, "Core"),
    ]
    offerings = [_offering("need", "s-need", "Monday", "07:30", "11:10")]
    repos = build_repos(
        current_semester=5,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        prereqs=[FakePrereq("need", "base")],
        offerings=offerings,
        track=FakeTrack(
            track_id="TRACK-STD-001",
            min_credits_per_term=4,
            min_courses=1,
        ),
    )
    plan = generate_semester_plan("S1", TERM, repos=repos)
    assert any(
        item.reason == ExclusionReason.DROPPED_PREREQ_BLOCKED
        for item in plan.exclusions
    )


def test_failed_assigned_uses_retake_after_fail_reason():
    courses = [FakeCourse("a1", "CSC10004", credits=4)]
    rows = [FakeCurrRow("a1", 2, "Core")]
    offerings = [_offering("a1", "s-a1", "Monday", "07:30", "11:10")]
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        attempts=[FakeAttempt("a1", 1, "Failed", grade=4.0)],
        offerings=offerings,
        track=FakeTrack(
            track_id="TRACK-STD-001",
            min_credits_per_term=4,
            min_courses=1,
        ),
    )
    plan = generate_semester_plan("S1", TERM, repos=repos)
    assert plan.items[0].selection_reason == SelectionReason.RETAKE_AFTER_FAIL


def test_blocked_and_missing_electives_appear_in_exclusions():
    courses = [
        FakeCourse("a1", "CSC10004", credits=4),
        FakeCourse("need", "BAA00021", credits=3),
        FakeCourse("miss", "BAA00022", credits=3),
        FakeCourse("ok", "PHY00001", credits=3),
        FakeCourse("wrong", "BAA00999", credits=3),
    ]
    rows = [
        FakeCurrRow("a1", 2, "Core"),
        FakeCurrRow("need", 2, "Elective"),
        FakeCurrRow("miss", 2, "Elective"),
        FakeCurrRow("ok", 2, "Elective"),
        FakeCurrRow("wrong", 1, "Elective"),
    ]
    offerings = [
        _offering("a1", "s-a1", "Monday", "07:30", "11:10"),
        _offering("need", "s-need", "Tuesday", "07:30", "09:30", "TH"),
        _offering("ok", "s-ok", "Wednesday", "07:30", "09:30", "TH"),
    ]
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        prereqs=[FakePrereq("need", "a1")],
        offerings=offerings,
        track=FakeTrack(
            track_id="TRACK-STD-001",
            min_credits_per_term=4,
            min_courses=1,
        ),
    )
    plan = generate_semester_plan("S1", TERM, repos=repos)
    by_code = {item.course_code: item.reason for item in plan.exclusions}
    assert by_code["BAA00021"] == ExclusionReason.DROPPED_PREREQ_BLOCKED
    assert by_code["BAA00022"] == ExclusionReason.DROPPED_NOT_OFFERED
    assert "BAA00999" not in by_code

from datetime import time

from tests.fakes import (
    FakeCourse,
    FakeCurrRow,
    build_repos,
    meeting,
    offering_with,
    section_with,
)

from app.deterministic.conflicts import detect_conflicts, intervals_overlap


def test_morning_lt_clashes_with_morning_late_th():
    """07:30–11:10 vs 09:30–11:30 overlap by 1h40 — the comparison to get right first."""
    assert intervals_overlap(time(7, 30), time(11, 10), time(9, 30), time(11, 30))


def test_touching_endpoints_do_not_clash():
    assert not intervals_overlap(time(7, 30), time(9, 30), time(9, 30), time(11, 30))


def test_detect_conflicts_reports_the_overlapping_interval():
    term_id = "TERM-2026-1"
    courses = [
        FakeCourse("c1", "CSC13010"),
        FakeCourse("c2", "CSC13005"),
    ]
    rows = [
        FakeCurrRow("c1", 8, "Core", "SE"),
        FakeCurrRow("c2", 8, "Core", "SE"),
    ]
    off1 = offering_with(
        "off-1",
        "c1",
        term_id,
        section_with("sec-lt", "off-1", "01", meeting("Monday", "07:30", "11:10", "LT")),
    )
    off2 = offering_with(
        "off-2",
        "c2",
        term_id,
        section_with("sec-th", "off-2", "01", meeting("Monday", "09:30", "11:30", "TH")),
    )
    repos = build_repos(
        current_semester=8,
        courses=courses,
        curr_rows=rows,
        offerings=[off1, off2],
    )
    pairs = detect_conflicts(["sec-lt", "sec-th"], repos=repos)
    assert len(pairs) == 1
    assert pairs[0].day_of_week == "Monday"
    assert pairs[0].overlap_start == time(9, 30)
    assert pairs[0].overlap_end == time(11, 10)


def test_back_to_back_practicals_are_both_takeable():
    term_id = "TERM-2026-1"
    courses = [FakeCourse("c1", "CSC1"), FakeCourse("c2", "CSC2")]
    rows = [FakeCurrRow("c1", 2, "Core"), FakeCurrRow("c2", 2, "Core")]
    off1 = offering_with(
        "off-1",
        "c1",
        term_id,
        section_with("sec-a", "off-1", "01", meeting("Wednesday", "07:30", "09:30", "TH")),
    )
    off2 = offering_with(
        "off-2",
        "c2",
        term_id,
        section_with("sec-b", "off-2", "01", meeting("Wednesday", "09:30", "11:30", "TH")),
    )
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        offerings=[off1, off2],
    )
    assert detect_conflicts(["sec-a", "sec-b"], repos=repos) == []


def test_overlapping_lt_and_th_on_the_same_section_clash():
    term_id = "TERM-2026-1"
    courses = [FakeCourse("c1", "CSC1")]
    rows = [FakeCurrRow("c1", 2, "Core")]
    offering = offering_with(
        "off-1",
        "c1",
        term_id,
        section_with(
            "sec-mixed",
            "off-1",
            "01",
            meeting("Monday", "07:30", "11:10", "LT"),
            meeting("Monday", "09:30", "11:30", "TH"),
        ),
    )
    repos = build_repos(
        current_semester=2,
        spec_code=None,
        courses=courses,
        curr_rows=rows,
        offerings=[offering],
    )
    pairs = detect_conflicts(["sec-mixed"], repos=repos)
    assert len(pairs) == 1
    assert pairs[0].section_id_a == "sec-mixed"
    assert pairs[0].section_id_b == "sec-mixed"

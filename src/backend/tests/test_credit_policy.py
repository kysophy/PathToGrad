from tests.fakes import FakeCourse, FakeCurrRow, FakeTrack, build_repos

from app.deterministic.credit_policy import validate_credit_load
from app.deterministic.types import TermType, ToolStatus


def _repos(track: FakeTrack | None = None):
    track = track or FakeTrack(track_id="TRACK-STD-001")
    return build_repos(
        courses=[FakeCourse("c1", "CSC10012")],
        curr_rows=[FakeCurrRow("c1", 1, "Core")],
        track=track,
    )


def test_reads_limits_from_track_not_hardcoded():
    track = FakeTrack(
        track_id="TRACK-OTHER",
        min_credits_per_term=12,
        max_credits_per_term=20,
        min_courses=3,
        max_courses=5,
    )
    result = validate_credit_load(
        "TRACK-OTHER", "Semester2", 15, repos=_repos(track)
    )
    assert result.min_credits == 12
    assert result.max_credits == 20
    assert result.min_courses == 3
    assert result.max_courses == 5
    assert result.within_limits is True
    assert result.term_type is TermType.SEMESTER_2


def test_under_min_and_over_max():
    repos = _repos()
    low = validate_credit_load("TRACK-STD-001", "Summer", 10, repos=repos)
    high = validate_credit_load("TRACK-STD-001", "Summer", 25, repos=repos)
    assert low.within_limits is False
    assert high.within_limits is False
    assert low.min_credits == 14
    assert high.max_credits == 24


def test_unknown_track_is_uncertain():
    result = validate_credit_load("NOPE", "Semester1", 16, repos=_repos())
    assert result.status == ToolStatus.UNCERTAIN
    assert result.within_limits is False

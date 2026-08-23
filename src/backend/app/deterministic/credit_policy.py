"""Credit policy validator (A-15).

Min/max come from PROGRAM_TRACK — never hardcoded. Summer uses the same
limits; `term_type` stays on the signature so a later override would not
change callers.
"""

from app.deterministic.ports import PlanningRepos
from app.deterministic.types import TermType, ToolStatus
from app.schemas.tools import CreditPolicyResult


def validate_credit_load(
    track_id: str,
    term_type: str,
    total_credits: int,
    *,
    repos: PlanningRepos,
) -> CreditPolicyResult:
    track = repos.curriculum.get_track(track_id)
    try:
        slot = TermType(term_type) if not isinstance(term_type, TermType) else term_type
    except ValueError:
        slot = TermType.SEMESTER_2
        return CreditPolicyResult(
            track_id=track_id,
            term_type=slot,
            total_credits=total_credits,
            min_credits=0,
            max_credits=0,
            min_courses=0,
            max_courses=0,
            within_limits=False,
            status=ToolStatus.UNCERTAIN,
            warnings=[f"Unknown term_type {term_type!r}."],
        )

    if track is None:
        return CreditPolicyResult(
            track_id=track_id,
            term_type=slot,
            total_credits=total_credits,
            min_credits=0,
            max_credits=0,
            min_courses=0,
            max_courses=0,
            within_limits=False,
            status=ToolStatus.UNCERTAIN,
            warnings=[f"Program track {track_id} was not found."],
        )

    within = track.min_credits_per_term <= total_credits <= track.max_credits_per_term
    return CreditPolicyResult(
        track_id=track.track_id,
        term_type=slot,
        total_credits=total_credits,
        min_credits=track.min_credits_per_term,
        max_credits=track.max_credits_per_term,
        min_courses=track.min_courses,
        max_courses=track.max_courses,
        within_limits=within,
        status=ToolStatus.OK,
    )

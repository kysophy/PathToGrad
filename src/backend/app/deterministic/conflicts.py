"""Timetable conflict detector (A-14).

Two meetings clash when they share a day and the half-open intervals overlap:

    a.start < b.end AND b.start < a.end

Touching endpoints do **not** clash. That is how back-to-back practicals
(07:30–09:30 then 09:30–11:30) both fit. A morning LT 07:30–11:10 against a
morning-late TH 09:30–11:30 overlaps by 1h40 and **does** clash.
"""

from datetime import time

from app.deterministic.ports import PlanningRepos
from app.schemas.tools import ConflictPair


def intervals_overlap(start_a: time, end_a: time, start_b: time, end_b: time) -> bool:
    return start_a < end_b and start_b < end_a


def overlap_interval(
    start_a: time,
    end_a: time,
    start_b: time,
    end_b: time,
) -> tuple[time, time]:
    return max(start_a, start_b), min(end_a, end_b)


def detect_conflicts(
    section_ids: list[str],
    *,
    repos: PlanningRepos,
) -> list[ConflictPair]:
    meetings_by_section: dict[str, list] = {}
    for section_id in section_ids:
        meetings_by_section[section_id] = list(repos.offerings.get_meetings(section_id))

    pairs: list[ConflictPair] = []
    seen: set[tuple[str, str, str, time, time]] = set()
    def add_pair(left_id: str, right_id: str, left, right) -> None:
        if left.day_of_week != right.day_of_week:
            return
        if not intervals_overlap(
            left.start_time,
            left.end_time,
            right.start_time,
            right.end_time,
        ):
            return
        overlap_start, overlap_end = overlap_interval(
            left.start_time,
            left.end_time,
            right.start_time,
            right.end_time,
        )
        a_id, b_id = sorted((left_id, right_id))
        key = (a_id, b_id, left.day_of_week, overlap_start, overlap_end)
        if key in seen:
            return
        seen.add(key)
        pairs.append(
            ConflictPair(
                section_id_a=a_id,
                section_id_b=b_id,
                day_of_week=left.day_of_week,
                overlap_start=overlap_start,
                overlap_end=overlap_end,
            )
        )

    unique_ids = list(dict.fromkeys(section_ids))
    for section_id in unique_ids:
        meetings = meetings_by_section[section_id]
        for i, left in enumerate(meetings):
            for right in meetings[i + 1 :]:
                add_pair(section_id, section_id, left, right)

    for i, left_id in enumerate(unique_ids):
        for right_id in unique_ids[i + 1 :]:
            for left in meetings_by_section[left_id]:
                for right in meetings_by_section[right_id]:
                    add_pair(left_id, right_id, left, right)
    return pairs

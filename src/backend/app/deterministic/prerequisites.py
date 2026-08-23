"""Prerequisite checker (A-11) and public cycle detector (A-12).

Khoa's CSV validator imports `find_prerequisite_cycles` with an `edges` list
built from the file — no database required. A-11 loads edges from the course
repository and calls the same function so a circular graph cannot hang.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from app.deterministic.ports import PlanningRepos
from app.deterministic.types import ToolStatus
from app.schemas.tools import PrerequisiteItem, PrerequisiteResult

_WHITE, _GRAY, _BLACK = 0, 1, 2


def find_prerequisite_cycles(
    course_ids: list[str] | None = None,
    edges: Sequence[tuple[str, str]] | None = None,
) -> list[list[str]]:
    """DFS with colour marking. Each cycle is the node list, closed at the end.

    `edges` is `(course, required_course)` using whatever identifiers the
    caller has (codes from a CSV, or database ids). `course_ids` optionally
    restricts the subgraph.
    """
    if not edges:
        return []

    allowed = set(course_ids) if course_ids is not None else None
    graph: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for source, required in edges:
        # Keep an edge if *either* end is in the requested set. Requiring
        # both ends dropped A ⇄ B when a tool call only named A.
        if allowed is not None and source not in allowed and required not in allowed:
            continue
        graph[source].append(required)
        nodes.add(source)
        nodes.add(required)

    colour: dict[str, int] = {}
    cycles: list[list[str]] = []

    def dfs(node: str, path: list[str]) -> None:
        colour[node] = _GRAY
        path.append(node)
        for nxt in graph[node]:
            state = colour.get(nxt, _WHITE)
            if state == _WHITE:
                dfs(nxt, path)
            elif state == _GRAY:
                start = path.index(nxt)
                cycles.append(path[start:] + [nxt])
        path.pop()
        colour[node] = _BLACK

    for node in sorted(nodes):
        if colour.get(node, _WHITE) == _WHITE:
            dfs(node, [])
    return cycles


def _attempt_status(attempts: list) -> tuple[str, bool | None, str | None]:
    """Return (label, satisfied, warning) for one required course."""
    if not attempts:
        return "Missing", False, None

    latest = max(attempts, key=lambda item: item.attempt_number)
    status = latest.result_status
    grade = latest.grade
    if grade is not None:
        try:
            grade = float(grade)
        except (TypeError, ValueError):
            grade = None

    if status == "Passed" and grade is not None:
        return "Passed", True, None
    if status == "Passed" and grade is None:
        return (
            "Unknown",
            None,
            "Passed attempt has no grade, so eligibility cannot be verified.",
        )
    if status == "Failed":
        return "Failed", False, None
    if status == "InProgress":
        return "InProgress", False, None
    return "Unknown", None, f"Attempt status {status!r} cannot be verified."


def check_prerequisites(
    student_id: str,
    course_ids: list[str],
    *,
    repos: PlanningRepos,
) -> list[PrerequisiteResult]:
    profile = repos.students.get_with_policy(student_id)
    record = repos.attempts.get_record(student_id)

    graph_rows = repos.courses.get_graph(course_ids or None)
    edges = [(row.course_id, row.required_course_id) for row in graph_rows]
    cycles = find_prerequisite_cycles(course_ids=course_ids or None, edges=edges)
    cycles_by_course: dict[str, list[str]] = {}
    for loop in cycles:
        pretty = (
            f"Circular prerequisite cycle {' -> '.join(loop)}. "
            "Eligibility cannot be verified."
        )
        for node in dict.fromkeys(loop):
            cycles_by_course.setdefault(node, []).append(pretty)

    results: list[PrerequisiteResult] = []
    for course_id in course_ids:
        course = repos.courses.get_by_id(course_id)
        if course is None:
            results.append(
                PrerequisiteResult(
                    course_id=course_id,
                    course_code=course_id,
                    satisfied=None,
                    status=ToolStatus.UNCERTAIN,
                    warnings=["Course is not in the catalogue."],
                )
            )
            continue

        if profile is None:
            results.append(
                PrerequisiteResult(
                    course_id=course.course_id,
                    course_code=course.course_code,
                    satisfied=None,
                    status=ToolStatus.UNCERTAIN,
                    warnings=[f"Student {student_id} was not found."],
                )
            )
            continue

        required_courses = repos.courses.get_prerequisites(course_id)
        items: list[PrerequisiteItem] = []
        missing: list[PrerequisiteItem] = []
        warnings: list[str] = []
        any_uncertain = False
        any_unmet = False

        for required in required_courses:
            attempts = []
            if record is not None:
                attempts = repos.attempts.list_for_course(
                    record.record_id, required.course_id
                )
            label, satisfied, warning = _attempt_status(attempts)
            item = PrerequisiteItem(
                course_id=required.course_id,
                course_code=required.course_code,
                name_en=required.name_en,
                satisfied=satisfied,
                attempt_status=label,
                warning=warning,
            )
            items.append(item)
            if warning:
                warnings.append(f"{required.course_code}: {warning}")
                any_uncertain = True
            if satisfied is False:
                any_unmet = True
                missing.append(item)
            elif satisfied is None:
                any_uncertain = True
                missing.append(item)

        for text in cycles_by_course.get(course_id, []):
            warnings.append(text)
            any_uncertain = True

        if any_uncertain:
            overall: bool | None = None
            status = ToolStatus.UNCERTAIN
        elif any_unmet:
            overall = False
            status = ToolStatus.OK
        else:
            overall = True
            status = ToolStatus.OK

        results.append(
            PrerequisiteResult(
                course_id=course.course_id,
                course_code=course.course_code,
                satisfied=overall,
                missing=missing,
                prerequisites=items,
                status=status,
                warnings=warnings,
            )
        )
    return results

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AttemptSnapshot:
    attempt_number: int

    result_status: str

    grade: float | None


@dataclass(frozen=True)
class PrerequisiteEvaluation:
    status: str

    satisfied: bool | None

    warning: str | None = None


def evaluate_attempts(
    attempts: Iterable[AttemptSnapshot],
) -> PrerequisiteEvaluation:

    attempt_list = list(attempts)

    if not attempt_list:
        return PrerequisiteEvaluation(
            status="Missing",
            satisfied=False,
        )

    verified_pass = any(
        attempt.result_status == "Passed"
        and attempt.grade is not None
        for attempt in attempt_list
    )

    if verified_pass:
        return PrerequisiteEvaluation(
            status="Passed",
            satisfied=True,
        )

    incomplete_pass = any(
        attempt.result_status == "Passed"
        and attempt.grade is None
        for attempt in attempt_list
    )

    if incomplete_pass:
        return PrerequisiteEvaluation(
            status="Unknown",
            satisfied=None,
            warning=(
                "A Passed prerequisite attempt is "
                "incomplete because its grade "
                "cannot be verified."
            ),
        )

    latest_attempt = max(
        attempt_list,
        key=lambda attempt: (
            attempt.attempt_number
        ),
    )

    if latest_attempt.result_status == "InProgress":
        return PrerequisiteEvaluation(
            status="InProgress",
            satisfied=False,
        )

    if latest_attempt.result_status == "Failed":
        return PrerequisiteEvaluation(
            status="Failed",
            satisfied=False,
        )

    return PrerequisiteEvaluation(
        status="Unknown",
        satisfied=None,
        warning=(
            "Prerequisite attempt data uses "
            "an unsupported or unverifiable status."
        ),
    )


def combine_prerequisites(
    evaluations: Iterable[
        PrerequisiteEvaluation
    ],
) -> bool | None:

    evaluation_list = list(
        evaluations
    )

    if any(
        item.satisfied is None
        for item in evaluation_list
    ):
        return None

    return all(
        item.satisfied is True
        for item in evaluation_list
    )
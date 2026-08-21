from app.deterministic.prerequisite_checker import (
    AttemptSnapshot,
    combine_prerequisites,
    evaluate_attempts,
)


def test_missing_prerequisite_attempt():
    result = evaluate_attempts([])

    assert result.status == "Missing"

    assert result.satisfied is False


def test_verified_pass_satisfies_prerequisite():
    result = evaluate_attempts(
        [
            AttemptSnapshot(
                attempt_number=1,
                result_status="Passed",
                grade=8.0,
            ),
        ]
    )

    assert result.status == "Passed"

    assert result.satisfied is True


def test_failed_prerequisite():
    result = evaluate_attempts(
        [
            AttemptSnapshot(
                attempt_number=1,
                result_status="Failed",
                grade=4.0,
            ),
        ]
    )

    assert result.status == "Failed"

    assert result.satisfied is False


def test_in_progress_prerequisite():
    result = evaluate_attempts(
        [
            AttemptSnapshot(
                attempt_number=1,
                result_status="InProgress",
                grade=None,
            ),
        ]
    )

    assert result.status == "InProgress"

    assert result.satisfied is False


def test_incomplete_pass_is_uncertain():
    result = evaluate_attempts(
        [
            AttemptSnapshot(
                attempt_number=1,
                result_status="Passed",
                grade=None,
            ),
        ]
    )

    assert result.status == "Unknown"

    assert result.satisfied is None

    assert result.warning is not None


def test_uncertain_rule_makes_overall_uncertain():
    overall = combine_prerequisites(
        [
            evaluate_attempts(
                [
                    AttemptSnapshot(
                        attempt_number=1,
                        result_status="Passed",
                        grade=8.0,
                    ),
                ]
            ),

            evaluate_attempts(
                [
                    AttemptSnapshot(
                        attempt_number=1,
                        result_status="Passed",
                        grade=None,
                    ),
                ]
            ),
        ]
    )

    assert overall is None
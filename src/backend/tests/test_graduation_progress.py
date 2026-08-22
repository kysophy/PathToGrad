from app.deterministic.graduation_progress import (
    CompletedCourse,
    calculate_graduation_progress,
)


def test_mixed_passed_courses_only():
    result = calculate_graduation_progress(
        completed_courses=[
            CompletedCourse(
                "CSC00004",
                4,
            ),
        ],

        required_credits=6,

        required_course_codes=[
            "CSC00004",
            "CSC10009",
        ],
    )

    assert result.earned_credits == 4

    assert result.remaining_credits == 2

    assert result.completed is False

    assert (
        result.missing_required_courses
        == ["CSC10009"]
    )


def test_credit_boundary_below_requirement():
    result = calculate_graduation_progress(
        completed_courses=[
            CompletedCourse(
                "TEST-A",
                5,
            ),
        ],

        required_credits=6,

        required_course_codes=[],
    )

    assert (
        result.credit_requirement_met
        is False
    )


def test_credit_boundary_exact_requirement():
    result = calculate_graduation_progress(
        completed_courses=[
            CompletedCourse(
                "TEST-A",
                6,
            ),
        ],

        required_credits=6,

        required_course_codes=[],
    )

    assert (
        result.credit_requirement_met
        is True
    )


def test_missing_required_course_blocks_completion():
    result = calculate_graduation_progress(
        completed_courses=[
            CompletedCourse(
                "OTHER",
                6,
            ),
        ],

        required_credits=6,

        required_course_codes=[
            "REQUIRED",
        ],
    )

    assert (
        result.credit_requirement_met
        is True
    )

    assert (
        result.missing_required_courses
        == ["REQUIRED"]
    )

    assert result.completed is False


def test_complete_when_all_requirements_met():
    result = calculate_graduation_progress(
        completed_courses=[
            CompletedCourse(
                "CSC00004",
                4,
            ),

            CompletedCourse(
                "CSC10009",
                2,
            ),
        ],

        required_credits=6,

        required_course_codes=[
            "CSC00004",
            "CSC10009",
        ],
    )

    assert (
        result.missing_required_courses
        == []
    )

    assert result.completed is True
"""NFR-06 / NEW-TC-51: every code in the prose must already be allowed."""

from app.llm.guard import extract_course_codes, prose_is_allowed


def test_extracts_known_prefixes():
    text = "Take CSC10004 and MTH00008; skip BAA00004 and PHY00005."
    assert extract_course_codes(text) == {
        "CSC10004",
        "MTH00008",
        "BAA00004",
        "PHY00005",
    }


def test_honest_plan_prose_passes():
    prose = "CSC10004 is assigned this semester. CSC10012 was excluded."
    allowed = {"CSC10004", "CSC10012"}
    assert prose_is_allowed(prose, allowed)


def test_hallucinated_code_is_rejected():
    prose = "Also take CSC99999 because it is popular."
    allowed = {"CSC10004", "CSC10012"}
    assert not prose_is_allowed(prose, allowed)


def test_empty_prose_with_empty_allow_list_passes():
    assert prose_is_allowed("No course codes here.", set())

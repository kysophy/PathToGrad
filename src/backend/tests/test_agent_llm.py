"""Agent orchestration: engine still wins when the model is wrong or late."""

from app.llm.guard import extract_course_codes
from app.llm.provider import LLMProviderAdapter
from app.schemas.enums import SelectionReason
from app.services.agent_service import AgentService, classify_message
from tests.fakes import (
    FakeCourse,
    FakeCurrRow,
    build_repos,
    meeting,
    offering_with,
    section_with,
)

TERM = "TERM-2026-1"


def _repos():
    courses = [
        FakeCourse(
            "a1",
            "CSC10004",
            name_vi="Cấu trúc dữ liệu và giải thuật",
            name_en="Data Structures and Algorithms",
            credits=4,
        ),
        FakeCourse("a2", "CSC10009", name_en="Computer Systems", credits=4),
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
        offering_with(
            "off-a1",
            "a1",
            TERM,
            section_with("s-a1", "off-a1", "01", meeting("Monday", "07:30", "11:10")),
        ),
        offering_with(
            "off-a2",
            "a2",
            TERM,
            section_with("s-a2", "off-a2", "01", meeting("Tuesday", "07:30", "11:10")),
        ),
        offering_with(
            "off-e1",
            "e1",
            TERM,
            section_with("s-e1", "off-e1", "01", meeting("Wednesday", "07:30", "09:30", "TH")),
        ),
        offering_with(
            "off-e2",
            "e2",
            TERM,
            section_with("s-e2", "off-e2", "01", meeting("Thursday", "07:30", "09:30", "TH")),
        ),
        offering_with(
            "off-e3",
            "e3",
            TERM,
            section_with("s-e3", "off-e3", "01", meeting("Friday", "07:30", "09:30", "TH")),
        ),
    ]
    return build_repos(
        current_semester=2,
        spec_code=None,
        target_credit_load=18,
        courses=courses,
        curr_rows=rows,
        offerings=offerings,
    )


def test_timeout_still_returns_engine_items():
    def boom(_prompt, _system=None):
        raise TimeoutError("slow")

    service = AgentService(
        repos=_repos(),
        provider=LLMProviderAdapter(api_key="", generate_fn=boom),
    )
    result = service.generate_plan(
        "S1",
        TERM,
        target_credit_load=18,
        note="please keep the load near 18",
    )
    assert result.items
    assert any(
        item.selection_reason == SelectionReason.ASSIGNED_THIS_SEMESTER
        for item in result.items
    )
    assert result.explanation_source == "template"
    assert "CSC10004" in result.explanation


def test_bad_prose_replaced_by_template():
    def liar(_prompt, _system=None):
        if "Extract JSON" in _prompt:
            return '{"target_credit_load": 18, "include_retakes": true}'
        return "You should also take CSC99999, it is famous."

    service = AgentService(
        repos=_repos(),
        provider=LLMProviderAdapter(api_key="fake", generate_fn=liar),
    )
    result = service.generate_plan("S1", TERM, note="aim for 18 credits")
    assert result.explanation_source == "template"
    assert "CSC99999" not in result.explanation
    codes = {item.course_code for item in result.items}
    assert "CSC10004" in codes


def test_chat_unknown_course_does_not_invent():
    service = AgentService(
        repos=_repos(),
        provider=LLMProviderAdapter(api_key=""),
    )
    reply = service.chat("What is CSC99999?", student_id="S1", term_id=TERM)
    assert reply.used_template is True
    assert "CSC99999" in reply.reply
    assert "will not invent" in reply.reply


def test_chat_known_course_uses_template_without_key():
    service = AgentService(
        repos=_repos(),
        provider=LLMProviderAdapter(api_key=""),
    )
    reply = service.chat("What is CSC10004 about?", student_id="S1", term_id=TERM)
    assert reply.intent == "course"
    assert "CSC10004" in reply.reply
    assert "Cấu trúc dữ liệu và giải thuật (Data Structures and Algorithms)" in reply.reply
    assert "illustrative, not the official syllabus" in reply.reply
    assert reply.used_template is True


def test_weather_is_refuse_with_no_course_codes():
    assert classify_message("what is the weather") == "refuse"
    service = AgentService(
        repos=_repos(),
        provider=LLMProviderAdapter(api_key=""),
    )
    reply = service.chat("what is the weather", student_id="S1", term_id=TERM)
    assert reply.intent == "refuse"
    assert extract_course_codes(reply.reply) == set()
    assert "cannot register you" in reply.reply or "cannot" in reply.reply.lower()

"""Three-stage agent: LLM intent/explain, engine plan, template fallback."""

from __future__ import annotations

import json
import logging
import re
import time
from uuid import uuid4

from typing import Literal

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.deterministic.catalog import get_course_catalog
from app.deterministic.generator import generate_semester_plan
from app.deterministic.ports import PlanningRepos
from app.deterministic.risks import detect_risks
from app.llm import briefs, prompts, templates
from app.llm.guard import extract_course_codes, prose_is_allowed
from app.llm.provider import (
    LLMProviderAdapter,
    ProviderError,
    ProviderUnavailable,
)
from app.models.agent import AgentRun, ToolCall
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.curriculum_repository import CurriculumRepository
from app.repositories.offering_repository import OfferingRepository
from app.repositories.student_repository import StudentRepository
from app.schemas.agent import (
    ChatResponse,
    ExplainedPlanResponse,
    RecommendedCourseView,
)
from app.schemas.enums import AgentRunStatus, CoursePrimaryStatus, GenerationMode
from app.schemas.tools import GeneratedPlan, PlanRequest, Risk

logger = logging.getLogger(__name__)

_PLAN_WORDS = (
    "plan",
    "generate",
    "schedule",
    "what should i take",
    "what do i take",
    "recommend",
    "this term",
    "this semester",
)
_RISK_WORDS = ("risk", "gpa", "fail", "backlog", "danger", "warning")
_GREET_RE = re.compile(r"^\s*(hi|hello|hey|yo)\b", re.IGNORECASE)


def planning_repos(db: Session) -> PlanningRepos:
    return PlanningRepos(
        students=StudentRepository(db),
        courses=CourseRepository(db),
        curriculum=CurriculumRepository(db),
        attempts=AttemptRepository(db),
        offerings=OfferingRepository(db),
    )


ChatIntent = Literal["plan", "course", "risk", "greet", "refuse"]


def classify_message(message: str) -> ChatIntent:
    text = message.strip()
    lower = text.lower()
    if _GREET_RE.match(text) and len(text) < 40:
        return "greet"
    codes = extract_course_codes(text)
    if codes:
        return "course"
    if any(word in lower for word in _RISK_WORDS):
        return "risk"
    if any(word in lower for word in _PLAN_WORDS):
        return "plan"
    return "refuse"


def _plan_allow_list(plan: GeneratedPlan, risks: list[Risk]) -> set[str]:
    allowed = {item.course_code for item in plan.items}
    allowed.update(item.course_code for item in plan.exclusions)
    for risk in risks:
        allowed.update(risk.course_codes)
    return allowed


def _strip_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"```$", "", stripped)
    return stripped.strip()


class AgentService:
    def __init__(
        self,
        db: Session | None = None,
        repos: PlanningRepos | None = None,
        provider: LLMProviderAdapter | None = None,
    ) -> None:
        self.db = db
        self.repos = repos if repos is not None else (
            planning_repos(db) if db is not None else None
        )
        self.provider = provider or LLMProviderAdapter()
        self.settings = get_settings()

    def generate_plan(
        self,
        student_id: str,
        term_id: str | None = None,
        *,
        target_credit_load: int | None = None,
        include_retakes: bool = True,
        note: str | None = None,
    ) -> ExplainedPlanResponse:
        started = time.perf_counter()
        term_id = term_id or self.settings.DEFAULT_TERM_ID
        if self.repos is None:
            raise RuntimeError("AgentService needs a Session or fake repos")

        form = PlanRequest(
            target_credit_load=target_credit_load,
            include_retakes=include_retakes,
        )
        request, stage1_mode = self._parse_intent(
            student_id, term_id, note, form
        )
        plan, plan_ms = self._timed(
            lambda: generate_semester_plan(
                student_id, term_id, request, repos=self.repos
            )
        )
        risks, risk_ms = self._timed(
            lambda: detect_risks(
                student_id, plan, repos=self.repos, term_id=term_id
            )
        )
        catalog = get_course_catalog(student_id, term_id, repos=self.repos)
        names_en = {row.course_code: row.name_en for row in catalog.courses}
        names_vi = {row.course_code: row.name_vi for row in catalog.courses}
        explanation, source, stage3_mode = self._explain(
            plan, risks, names_en=names_en, names_vi=names_vi
        )

        run_id = self._log(
            student_id=student_id,
            generation_mode=(
                GenerationMode.LLM
                if stage1_mode == GenerationMode.LLM
                or stage3_mode == GenerationMode.LLM
                else GenerationMode.FALLBACK
            ),
            status=(
                AgentRunStatus.FALLBACK
                if source == "template"
                else AgentRunStatus.COMPLETED
            ),
            latency_ms=int((time.perf_counter() - started) * 1000),
            error=None if source == "llm" else "template explanation",
            tool_calls=[
                ("generate_semester_plan", request.model_dump(), plan.model_dump(mode="json"), plan_ms, True),
                ("detect_risks", {"student_id": student_id, "term_id": term_id}, [r.model_dump(mode="json") for r in risks], risk_ms, True),
            ],
        )
        names = names_en
        recommended = [
            RecommendedCourseView(
                course_code=row.course_code,
                course_name=row.name_en,
                note=(
                    "Assigned this semester"
                    if row.primary_status == CoursePrimaryStatus.ASSIGNED
                    else "Backlog"
                ),
            )
            for row in catalog.courses
            if row.primary_status
            in {CoursePrimaryStatus.ASSIGNED, CoursePrimaryStatus.BACKLOG}
        ]
        return ExplainedPlanResponse(
            student_id=plan.student_id,
            term_id=plan.term_id,
            generation_mode=plan.generation_mode,
            explanation_source=source,
            explanation=explanation,
            items=plan.items,
            exclusions=plan.exclusions,
            timetable=plan.timetable,
            total_credits=plan.total_credits,
            course_count=plan.course_count,
            warnings=plan.warnings,
            risks=risks,
            recommended=recommended,
            names=names,
            run_id=run_id,
            plan=plan,
        )

    def chat(
        self,
        message: str,
        *,
        student_id: str | None = None,
        term_id: str | None = None,
    ) -> ChatResponse:
        started = time.perf_counter()
        term_id = term_id or self.settings.DEFAULT_TERM_ID
        intent = classify_message(message)
        used_template = True
        mode = GenerationMode.FALLBACK
        reply = templates.REFUSE
        run_id = None

        if intent == "greet":
            reply = templates.GREETING
        elif intent == "course":
            reply, used_template, mode = self._course_reply(
                message, student_id, term_id
            )
        elif intent in {"plan", "risk"}:
            if not student_id:
                reply = (
                    "Sign in so I can generate a plan for you. "
                    "I still will not register you."
                )
            else:
                explained = self.generate_plan(student_id, term_id)
                reply = explained.explanation
                if intent == "risk" and explained.risks:
                    extra = "\n".join(
                        f"{risk.code.value}: {risk.message}"
                        for risk in explained.risks
                    )
                    if extra not in reply:
                        reply = reply + "\n" + extra
                used_template = explained.explanation_source == "template"
                mode = (
                    GenerationMode.LLM
                    if explained.explanation_source == "llm"
                    else GenerationMode.FALLBACK
                )
                run_id = explained.run_id
        else:
            reply = templates.REFUSE

        if run_id is None:
            run_id = self._log(
                student_id=student_id or "unknown",
                generation_mode=mode,
                status=(
                    AgentRunStatus.FALLBACK
                    if used_template
                    else AgentRunStatus.COMPLETED
                ),
                latency_ms=int((time.perf_counter() - started) * 1000),
                error=None,
                tool_calls=[],
            )
        return ChatResponse(
            reply=reply,
            intent=intent,
            generation_mode=mode,
            used_template=used_template,
            run_id=run_id,
        )

    def _parse_intent(
        self,
        student_id: str,
        term_id: str,
        note: str | None,
        form: PlanRequest,
    ) -> tuple[PlanRequest, GenerationMode]:
        if not note or not note.strip() or not self.provider.is_available():
            return form, GenerationMode.FALLBACK
        catalog = get_course_catalog(student_id, term_id, repos=self.repos)
        codes = ", ".join(sorted(row.course_code for row in catalog.courses)) or "(none)"
        prompt = prompts.INTENT_PROMPT.format(
            target_credits=form.target_credit_load,
            catalog_codes=codes,
            note=note.strip(),
        )
        try:
            raw = self.provider.generate(prompt, prompts.SYSTEM_PROMPT)
            data = json.loads(_strip_fence(raw))
            parsed = PlanRequest.model_validate(data)
            if parsed.target_credit_load is None:
                parsed = parsed.model_copy(
                    update={"target_credit_load": form.target_credit_load}
                )
            return parsed, GenerationMode.LLM
        except (ProviderError, ProviderUnavailable, ValueError, json.JSONDecodeError):
            return form, GenerationMode.FALLBACK

    def _explain(
        self,
        plan: GeneratedPlan,
        risks: list[Risk],
        *,
        names_en: dict[str, str] | None = None,
        names_vi: dict[str, str] | None = None,
    ) -> tuple[str, str, GenerationMode]:
        template = templates.explain_plan(
            plan, risks, names_en=names_en, names_vi=names_vi
        )
        allowed = _plan_allow_list(plan, risks)
        if not self.provider.is_available():
            return template, "template", GenerationMode.FALLBACK
        payload = {
            "items": [item.model_dump(mode="json") for item in plan.items],
            "exclusions": [item.model_dump(mode="json") for item in plan.exclusions],
            "total_credits": plan.total_credits,
            "course_count": plan.course_count,
            "warnings": plan.warnings,
            "risks": [risk.model_dump(mode="json") for risk in risks],
        }
        prompt = prompts.EXPLAIN_PROMPT.format(
            plan_json=json.dumps(payload, ensure_ascii=False)
        )
        try:
            prose = self.provider.generate(prompt, prompts.SYSTEM_PROMPT)
        except (ProviderError, ProviderUnavailable):
            return template, "template", GenerationMode.FALLBACK
        if not prose_is_allowed(prose, allowed):
            logger.warning("Stage-3 guard fired; discarding provider prose")
            return template, "template", GenerationMode.FALLBACK
        return prose, "llm", GenerationMode.LLM

    def _course_reply(
        self,
        message: str,
        student_id: str | None,
        term_id: str,
    ) -> tuple[str, bool, GenerationMode]:
        codes = list(extract_course_codes(message))
        code = codes[0]
        row = None
        course = None
        catalog_codes: set[str] = set()
        prereqs: list[str] = []
        if self.repos is not None:
            course = self.repos.courses.get_by_code(code)
            if course is not None:
                prereqs = [
                    req.course_code
                    for req in self.repos.courses.get_prerequisites(course.course_id)
                ]
            if student_id:
                catalog = get_course_catalog(
                    student_id, term_id, repos=self.repos
                )
                catalog_codes = {item.course_code for item in catalog.courses}
                for item in catalog.courses:
                    if item.course_code.upper() == code:
                        row = item
                        break
            if course is None and row is None and get_brief_entry(code) is None:
                return templates.unknown_course(code), True, GenerationMode.FALLBACK

        brief_row = get_brief_entry(code)
        if course is None and row is None and brief_row is None:
            return templates.unknown_course(code), True, GenerationMode.FALLBACK

        facts = {
            "course_code": code,
            "name_en": (
                row.name_en if row is not None else (brief_row or {}).get("name_en")
            ),
            "name_vi": (
                row.name_vi if row is not None else (brief_row or {}).get("name_vi")
            ),
            "credits": (
                row.credits if row is not None else (brief_row or {}).get("credits")
            ),
            "assigned_semester": (
                row.assigned_semester if row is not None else None
            ),
            "primary_status": (
                row.primary_status.value if row is not None else None
            ),
            "offered": (not row.not_offered) if row is not None else None,
            "blocked": row.blocked if row is not None else None,
            "prerequisites": prereqs,
            "brief": (brief_row or {}).get("brief"),
        }
        template = templates.explain_course(
            code,
            name_en=facts["name_en"],
            name_vi=facts["name_vi"],
            credits=facts["credits"],
            brief=facts["brief"],
            prereq_codes=prereqs,
            assigned_semester=facts["assigned_semester"],
            offered=facts["offered"],
            blocked=facts["blocked"],
            primary_status=facts["primary_status"],
        )
        allowed = {code}
        allowed.update(prereqs)
        allowed.update(catalog_codes)
        allowed.update(extract_course_codes(facts["brief"] or ""))
        if not self.provider.is_available():
            return template, True, GenerationMode.FALLBACK
        prompt = prompts.COURSE_QA_PROMPT.format(
            course_json=json.dumps(facts, ensure_ascii=False),
            message=message,
        )
        try:
            prose = self.provider.generate(prompt, prompts.SYSTEM_PROMPT)
        except (ProviderError, ProviderUnavailable):
            return template, True, GenerationMode.FALLBACK
        if not prose_is_allowed(prose, allowed):
            logger.warning("Course Q&A guard fired; discarding provider prose")
            return template, True, GenerationMode.FALLBACK
        return prose, False, GenerationMode.LLM

    def _log(
        self,
        *,
        student_id: str,
        generation_mode: GenerationMode,
        status: AgentRunStatus,
        latency_ms: int,
        error: str | None,
        tool_calls: list[tuple],
    ) -> str | None:
        run_id = str(uuid4())
        if self.db is None:
            return run_id
        try:
            if StudentRepository(self.db).get_profile(student_id) is None:
                return run_id
            self.db.add(
                AgentRun(
                    run_id=run_id,
                    student_id=student_id,
                    generation_mode=generation_mode.value,
                    provider="gemini" if self.provider.is_available() else None,
                    status=status.value,
                    latency_ms=latency_ms,
                    error=error,
                )
            )
            for name, input_json, output_json, duration_ms, success in tool_calls:
                self.db.add(
                    ToolCall(
                        tool_call_id=str(uuid4()),
                        run_id=run_id,
                        tool_name=name,
                        input_json=input_json,
                        output_json=output_json,
                        duration_ms=duration_ms,
                        success=success,
                    )
                )
            self.db.commit()
        except Exception:
            logger.exception("Could not write agent_run %s", run_id)
            try:
                self.db.rollback()
            except Exception:
                pass
        return run_id

    @staticmethod
    def _timed(fn):
        started = time.perf_counter()
        result = fn()
        return result, int((time.perf_counter() - started) * 1000)


def get_brief_entry(course_code: str) -> dict | None:
    return briefs.get_brief(course_code)

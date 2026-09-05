from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import AgentRunStatus, GenerationMode
from app.schemas.tools import GeneratedPlan, PlanExclusion, PlanItem, Risk, TimetableSlot


class AgentRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    run_id: str
    student_id: str
    generation_mode: GenerationMode
    provider: str | None
    status: AgentRunStatus
    latency_ms: int | None
    error: str | None
    created_at: datetime


class ToolCallRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tool_call_id: str
    run_id: str
    tool_name: str
    input_json: Any
    output_json: Any
    duration_ms: int | None
    success: bool
    created_at: datetime


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    student_id: str | None = None
    term_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    intent: Literal["plan", "course", "risk", "greet", "refuse"]
    generation_mode: GenerationMode
    used_template: bool
    run_id: str | None = None


class RecommendedCourseView(BaseModel):
    course_code: str
    course_name: str
    note: str


class PlanGenerateRequest(BaseModel):
    student_id: str
    term_id: str | None = None
    target_credit_load: int | None = None
    include_retakes: bool = True
    note: str | None = None


class ExplainedPlanResponse(BaseModel):
    student_id: str
    term_id: str
    generation_mode: GenerationMode
    explanation_source: Literal["llm", "template"]
    explanation: str
    items: list[PlanItem]
    exclusions: list[PlanExclusion]
    timetable: list[TimetableSlot]
    total_credits: int
    course_count: int
    warnings: list[str]
    risks: list[Risk]
    recommended: list[RecommendedCourseView]
    names: dict[str, str]
    run_id: str | None = None
    plan: GeneratedPlan

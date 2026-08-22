"""Tool input/output contracts for the deterministic engine (A-10–A-18).

Bodies are implemented in Part 3. Trâm's agent layer can import these now.
"""

from datetime import time

from pydantic import BaseModel, Field

from app.schemas.enums import (
    CoursePrimaryStatus,
    ExclusionReason,
    GenerationMode,
    RiskCode,
    RiskSeverity,
    SelectionReason,
    TermType,
    ToolStatus,
)


class ToolResult(BaseModel):
    status: ToolStatus = ToolStatus.OK
    warnings: list[str] = Field(default_factory=list)


class CatalogFilters(BaseModel):
    primary_status: CoursePrimaryStatus | None = None
    offered_only: bool = False


class CatalogCourse(BaseModel):
    course_id: str
    course_code: str
    name_vi: str
    name_en: str
    credits: int
    assigned_semester: int
    is_mandatory: bool
    spec_code: str | None
    primary_status: CoursePrimaryStatus
    blocked: bool = False
    not_offered: bool = False


class CatalogResult(ToolResult):
    student_id: str
    term_id: str
    courses: list[CatalogCourse] = Field(default_factory=list)


class PrerequisiteItem(BaseModel):
    course_id: str
    course_code: str
    name_en: str
    satisfied: bool | None
    attempt_status: str | None = None
    warning: str | None = None


class PrerequisiteResult(ToolResult):
    course_id: str
    course_code: str
    satisfied: bool | None = None
    missing: list[PrerequisiteItem] = Field(default_factory=list)
    prerequisites: list[PrerequisiteItem] = Field(default_factory=list)


class GraduationProgress(ToolResult):
    student_id: str
    earned_credits: int
    required_credits: int
    remaining_credits: int
    mandatory_passed: bool
    credit_requirement_met: bool
    missing_required_courses: list[str] = Field(default_factory=list)
    gpa: float | None = None
    completed: bool = False


class ConflictPair(BaseModel):
    section_id_a: str
    section_id_b: str
    day_of_week: str
    overlap_start: time
    overlap_end: time


class CreditPolicyResult(ToolResult):
    track_id: str
    term_type: TermType
    total_credits: int
    min_credits: int
    max_credits: int
    min_courses: int
    max_courses: int
    within_limits: bool


class PlanRequest(BaseModel):
    target_credit_load: int | None = None
    include_retakes: bool = True


class PlanItem(BaseModel):
    course_id: str
    course_code: str
    section_id: str
    credits: int
    selection_reason: SelectionReason


class PlanExclusion(BaseModel):
    course_id: str
    course_code: str
    reason: ExclusionReason


class TimetableSlot(BaseModel):
    section_id: str
    course_code: str
    meeting_type: str
    day_of_week: str
    start_time: time
    end_time: time
    room: str


class GeneratedPlan(ToolResult):
    student_id: str
    term_id: str
    generation_mode: GenerationMode = GenerationMode.FALLBACK
    items: list[PlanItem] = Field(default_factory=list)
    exclusions: list[PlanExclusion] = Field(default_factory=list)
    timetable: list[TimetableSlot] = Field(default_factory=list)
    total_credits: int = 0
    course_count: int = 0


class RetakeCandidate(BaseModel):
    course_id: str
    course_code: str
    last_grade: float | None
    last_result_status: str
    attempt_count: int
    eligible: bool
    offered_this_term: bool


class Risk(BaseModel):
    code: RiskCode
    severity: RiskSeverity
    message: str
    course_codes: list[str] = Field(default_factory=list)

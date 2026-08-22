from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import (
    GenerationMode,
    PlanStatus,
    ReviewDecision,
    SelectionReason,
)


class StudyPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plan_id: str
    student_id: str
    term_id: str
    version_number: int = Field(ge=1)
    status: PlanStatus
    generation_mode: GenerationMode
    target_credit_load: int
    total_credits: int
    previous_version_id: str | None
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None


class StudyPlanItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: str
    plan_id: str
    section_id: str
    selection_reason: SelectionReason


class PlanReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_id: str
    plan_id: str
    advisor_id: str
    decision: ReviewDecision
    comment: str | None
    review_at: datetime


class PlanReviewCreate(BaseModel):
    plan_id: str
    advisor_id: str
    decision: ReviewDecision
    comment: str | None = None

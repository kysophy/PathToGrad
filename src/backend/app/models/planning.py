from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.schemas.enums import GenerationMode, PlanStatus, ReviewDecision, SelectionReason

_enum_values = lambda cls: [item.value for item in cls]


class StudyPlan(Base):
    __tablename__ = "study_plan"

    __table_args__ = (
        CheckConstraint("version_number >= 1", name="chk_plan_version"),
        CheckConstraint("target_credit_load > 0", name="chk_plan_target_credits"),
        CheckConstraint("total_credits >= 0", name="chk_plan_total_credits"),
    )

    plan_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    student_id: Mapped[str] = mapped_column(
        ForeignKey("student_profile.student_id"),
        nullable=False,
    )

    term_id: Mapped[str] = mapped_column(
        ForeignKey("academic_term.term_id"),
        nullable=False,
    )

    version_number: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(
        Enum(*_enum_values(PlanStatus), name="plan_status"),
        nullable=False,
        default=PlanStatus.DRAFT.value,
    )

    generation_mode: Mapped[str] = mapped_column(
        Enum(*_enum_values(GenerationMode), name="generation_mode"),
        nullable=False,
    )

    target_credit_load: Mapped[int] = mapped_column(Integer, nullable=False)
    total_credits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    previous_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("study_plan.plan_id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    student: Mapped["StudentProfile"] = relationship("StudentProfile")
    term: Mapped["AcademicTerm"] = relationship("AcademicTerm")
    previous_version: Mapped[StudyPlan | None] = relationship(
        remote_side="StudyPlan.plan_id",
    )
    items: Mapped[list[StudyPlanItem]] = relationship(
        back_populates="plan",
    )
    reviews: Mapped[list[PlanReview]] = relationship(
        back_populates="plan",
    )


class StudyPlanItem(Base):
    __tablename__ = "study_plan_item"

    item_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    plan_id: Mapped[str] = mapped_column(
        ForeignKey("study_plan.plan_id"),
        nullable=False,
    )

    section_id: Mapped[str] = mapped_column(
        ForeignKey("class_section.section_id"),
        nullable=False,
    )

    selection_reason: Mapped[str] = mapped_column(
        Enum(*_enum_values(SelectionReason), name="selection_reason"),
        nullable=False,
    )

    plan: Mapped[StudyPlan] = relationship(back_populates="items")
    section: Mapped["ClassSection"] = relationship("ClassSection")


class PlanReview(Base):
    """Append-only advisor decision. Never update or delete rows."""

    __tablename__ = "plan_review"

    review_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    plan_id: Mapped[str] = mapped_column(
        ForeignKey("study_plan.plan_id"),
        nullable=False,
    )

    advisor_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
    )

    decision: Mapped[str] = mapped_column(
        Enum(*_enum_values(ReviewDecision), name="review_decision"),
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    review_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    plan: Mapped[StudyPlan] = relationship(back_populates="reviews")
    advisor: Mapped["User"] = relationship("User")

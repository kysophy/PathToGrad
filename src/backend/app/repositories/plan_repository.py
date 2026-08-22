from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import PlanReview, StudyPlan, StudyPlanItem


class PlanRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, plan_id: str) -> StudyPlan | None:
        return self.session.scalar(
            select(StudyPlan)
            .options(selectinload(StudyPlan.items))
            .where(StudyPlan.plan_id == plan_id)
        )

    def list_for_student(self, student_id: str) -> list[StudyPlan]:
        return list(
            self.session.scalars(
                select(StudyPlan)
                .options(selectinload(StudyPlan.items))
                .where(StudyPlan.student_id == student_id)
                .order_by(StudyPlan.version_number.desc())
            ).all()
        )

    def create(
        self,
        *,
        student_id: str,
        term_id: str,
        version_number: int,
        generation_mode: str,
        target_credit_load: int,
        total_credits: int = 0,
        previous_version_id: str | None = None,
        status: str = "Draft",
    ) -> StudyPlan:
        plan = StudyPlan(
            plan_id=str(uuid4()),
            student_id=student_id,
            term_id=term_id,
            version_number=version_number,
            status=status,
            generation_mode=generation_mode,
            target_credit_load=target_credit_load,
            total_credits=total_credits,
            previous_version_id=previous_version_id,
        )
        self.session.add(plan)
        self.session.flush()
        return plan

    def add_items(
        self,
        plan: StudyPlan,
        items: list[tuple[str, str]],
    ) -> list[StudyPlanItem]:
        """items is a list of (section_id, selection_reason)."""
        created: list[StudyPlanItem] = []
        for section_id, selection_reason in items:
            row = StudyPlanItem(
                item_id=str(uuid4()),
                plan_id=plan.plan_id,
                section_id=section_id,
                selection_reason=selection_reason,
            )
            self.session.add(row)
            created.append(row)
        self.session.flush()
        return created


class PlanReviewRepository:
    """Append-only. No update or delete methods by design (NFR-10)."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def insert(
        self,
        *,
        plan_id: str,
        advisor_id: str,
        decision: str,
        comment: str | None = None,
    ) -> PlanReview:
        review = PlanReview(
            review_id=str(uuid4()),
            plan_id=plan_id,
            advisor_id=advisor_id,
            decision=decision,
            comment=comment,
            review_at=datetime.utcnow(),
        )
        self.session.add(review)
        self.session.flush()
        return review

    def list_for_plan(self, plan_id: str) -> list[PlanReview]:
        return list(
            self.session.scalars(
                select(PlanReview)
                .where(PlanReview.plan_id == plan_id)
                .order_by(PlanReview.review_at)
            ).all()
        )

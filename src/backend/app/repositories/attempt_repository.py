from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    AcademicRecord,
    AcademicTerm,
    Course,
    CourseAttempt,
)


class AttemptRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_record(self, student_id: str) -> AcademicRecord | None:
        return self.session.scalar(
            select(AcademicRecord).where(
                AcademicRecord.student_id == student_id
            )
        )

    def list_for_student(self, student_id: str) -> list[CourseAttempt]:
        record = self.get_record(student_id)
        if record is None:
            return []
        return list(
            self.session.scalars(
                select(CourseAttempt)
                .where(CourseAttempt.record_id == record.record_id)
                .order_by(CourseAttempt.attempt_number)
            ).all()
        )

    def list_for_course(
        self,
        record_id: str,
        course_id: str,
    ) -> list[CourseAttempt]:
        return list(
            self.session.scalars(
                select(CourseAttempt)
                .where(
                    CourseAttempt.record_id == record_id,
                    CourseAttempt.course_id == course_id,
                )
                .order_by(CourseAttempt.attempt_number)
            ).all()
        )

    def latest_per_course(self, record_id: str) -> list[CourseAttempt]:
        attempts = list(
            self.session.scalars(
                select(CourseAttempt).where(
                    CourseAttempt.record_id == record_id
                )
            ).all()
        )
        latest: dict[str, CourseAttempt] = {}
        for attempt in attempts:
            current = latest.get(attempt.course_id)
            if (
                current is None
                or attempt.attempt_number > current.attempt_number
            ):
                latest[attempt.course_id] = attempt
        return list(latest.values())

    def get_verified_passed_courses(self, record_id: str):
        return self.session.execute(
            select(Course.course_code, Course.credits)
            .join(CourseAttempt, CourseAttempt.course_id == Course.course_id)
            .where(
                CourseAttempt.record_id == record_id,
                CourseAttempt.result_status == "Passed",
                CourseAttempt.grade.is_not(None),
            )
            .distinct()
            .order_by(Course.course_code)
        ).all()

    def get_attempt_rows(self, record_id: str):
        return self.session.execute(
            select(CourseAttempt, Course, AcademicTerm)
            .join(Course, Course.course_id == CourseAttempt.course_id)
            .join(
                AcademicTerm,
                AcademicTerm.term_id == CourseAttempt.term_id,
            )
            .where(CourseAttempt.record_id == record_id)
            .order_by(CourseAttempt.attempt_id)
        ).all()

    def add_attempt(
        self,
        *,
        record: AcademicRecord,
        course: Course,
        term: AcademicTerm,
        attempt_number: int,
        grade: float | None,
        result_status: str,
        credits_earned: int,
    ) -> CourseAttempt:
        attempt = CourseAttempt(
            attempt_id=str(uuid4()),
            record_id=record.record_id,
            course_id=course.course_id,
            term_id=term.term_id,
            attempt_number=attempt_number,
            grade=grade,
            result_status=result_status,
            credits_earned=credits_earned,
        )
        self.session.add(attempt)
        record.updated_at = datetime.utcnow()
        self.session.flush()
        return attempt

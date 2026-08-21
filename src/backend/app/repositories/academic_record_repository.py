import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academic import (
    AcademicRecord,
    AcademicTerm,
    Course,
    CourseAttempt,
)


class AcademicRecordRepository:

    @staticmethod
    def get_record(
        db: Session,
        student_id: str,
    ):
        return db.scalar(
            select(AcademicRecord).where(
                AcademicRecord.student_id == student_id
            )
        )


    @staticmethod
    def get_course_by_code(
        db: Session,
        course_code: str,
    ):
        return db.scalar(
            select(Course).where(
                Course.course_code == course_code
            )
        )


    @staticmethod
    def get_term(
        db: Session,
        term_id: str,
    ):
        return db.get(
            AcademicTerm,
            term_id,
        )


    @staticmethod
    def add_attempt(
        db: Session,
        *,
        record: AcademicRecord,
        course: Course,
        term: AcademicTerm,
        attempt_number: int,
        grade: float | None,
        result_status: str,
        credits_earned: int,
    ):

        attempt = CourseAttempt(
            attempt_id=str(uuid.uuid4()),
            record_id=record.record_id,
            course_id=course.course_id,
            term_id=term.term_id,
            attempt_number=attempt_number,
            grade=grade,
            result_status=result_status,
            credits_earned=credits_earned,
        )

        db.add(attempt)

        record.updated_at = datetime.utcnow()

        db.commit()

        return attempt


    @staticmethod
    def get_attempt_rows(
        db: Session,
        record_id: str,
    ):
        return db.execute(
            select(
                CourseAttempt,
                Course,
                AcademicTerm,
            )
            .join(
                Course,
                Course.course_id
                == CourseAttempt.course_id,
            )
            .join(
                AcademicTerm,
                AcademicTerm.term_id
                == CourseAttempt.term_id,
            )
            .where(
                CourseAttempt.record_id == record_id
            )
            .order_by(
                CourseAttempt.attempt_id
            )
        ).all()

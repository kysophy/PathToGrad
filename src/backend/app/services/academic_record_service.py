from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.academic_record_repository import (
    AcademicRecordRepository,
)
from app.repositories.profile_repository import ProfileRepository
from app.schemas.academic_record import (
    AcademicRecordResponse,
    CourseAttemptCreate,
    CourseAttemptResponse,
)


class AcademicRecordService:

    @staticmethod
    def _build_response(
        db: Session,
        record,
    ):
        rows = (
            AcademicRecordRepository.get_attempt_rows(
                db,
                record.record_id,
            )
        )

        attempts = []
        earned_credits = 0
        passed_courses = []

        for attempt, course, term in rows:

            if attempt.result_status == "Passed":
                earned_credits += attempt.credits_earned
                passed_courses.append(
                    course.course_code
                )

            attempts.append(
                CourseAttemptResponse(
                    attempt_id=attempt.attempt_id,

                    course_code=course.course_code,
                    course_name=course.course_name,

                    term_id=term.term_id,
                    term_name=term.name,

                    attempt_number=attempt.attempt_number,

                    grade=(
                        float(attempt.grade)
                        if attempt.grade is not None
                        else None
                    ),

                    result_status=attempt.result_status,

                    credits_earned=attempt.credits_earned,
                )
            )

        return AcademicRecordResponse(
            record_id=record.record_id,
            student_id=record.student_id,
            updated_at=record.updated_at,

            earned_credits=earned_credits,
            passed_courses=passed_courses,

            attempts=attempts,
        )


    @staticmethod
    def get(
        db: Session,
        student_id: str,
    ):

        profile = ProfileRepository.get_profile(
            db,
            student_id,
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Student profile does not exist. "
                    "Create the profile first."
                ),
            )

        record = AcademicRecordRepository.get_record(
            db,
            student_id,
        )

        if record is None:
            record = (
                ProfileRepository.ensure_academic_record(
                    db,
                    student_id,
                )
            )

            db.commit()

        return AcademicRecordService._build_response(
            db,
            record,
        )


    @staticmethod
    def add_attempt(
        db: Session,
        student_id: str,
        data: CourseAttemptCreate,
    ):

        profile = ProfileRepository.get_profile(
            db,
            student_id,
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Student profile does not exist. "
                    "Create the profile first."
                ),
            )

        course = (
            AcademicRecordRepository.get_course_by_code(
                db,
                data.course_code,
            )
        )

        if course is None:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Course {data.course_code} does not "
                    "exist in the course catalog."
                ),
            )

        term = AcademicRecordRepository.get_term(
            db,
            data.term_id,
        )

        if term is None:
            raise HTTPException(
                status_code=422,
                detail="Academic term does not exist.",
            )

        record = AcademicRecordRepository.get_record(
            db,
            student_id,
        )

        if record is None:
            record = (
                ProfileRepository.ensure_academic_record(
                    db,
                    student_id,
                )
            )

            db.flush()

        AcademicRecordRepository.add_attempt(
            db,
            record=record,
            course=course,
            term=term,
            attempt_number=data.attempt_number,
            grade=data.grade,
            result_status=data.result_status.value,
            credits_earned=data.credits_earned,
        )

        return AcademicRecordService._build_response(
            db,
            record,
        )

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academic import (
    AcademicProgram,
    AcademicRecord,
    Curriculum,
    CurriculumApplicability,
    Faculty,
    ProgramTrack,
    StudentProfile,
    User,
)


class ProfileRepository:

    @staticmethod
    def get_user(
        db: Session,
        user_id: str,
    ):
        return db.get(User, user_id)


    @staticmethod
    def get_profile(
        db: Session,
        student_id: str,
    ):
        return db.get(
            StudentProfile,
            student_id,
        )


    @staticmethod
    def get_program(
        db: Session,
        program_id: str,
    ):
        return db.get(
            AcademicProgram,
            program_id,
        )


    @staticmethod
    def get_faculty(
        db: Session,
        faculty_id: str,
    ):
        return db.get(
            Faculty,
            faculty_id,
        )


    @staticmethod
    def get_track(
        db: Session,
        track_id: str,
    ):
        return db.get(
            ProgramTrack,
            track_id,
        )


    @staticmethod
    def find_curriculum(
        db: Session,
        program_id: str,
        intake_year: int,
    ):
        statement = (
            select(Curriculum)
            .join(
                CurriculumApplicability,
                Curriculum.curriculum_id
                == CurriculumApplicability.curriculum_id,
            )
            .where(
                Curriculum.program_id == program_id,
                CurriculumApplicability.intake_year == intake_year,
            )
        )

        return db.scalar(statement)


    @staticmethod
    def save_profile(
        db: Session,
        *,
        student_id: str,
        user_id: str,
        program_id: str,
        intake_year: int,
        current_semester: int,
        target_credit_load: int,
    ):
        profile = db.get(
            StudentProfile,
            student_id,
        )

        if profile is None:
            profile = StudentProfile(
                student_id=student_id,
                user_id=user_id,
                program_id=program_id,
                intake_year=intake_year,
                current_semester=current_semester,
                target_credit_load=target_credit_load,
            )

            db.add(profile)

        else:
            profile.user_id = user_id
            profile.program_id = program_id
            profile.intake_year = intake_year
            profile.current_semester = current_semester
            profile.target_credit_load = target_credit_load

        db.flush()

        return profile


    @staticmethod
    def ensure_academic_record(
        db: Session,
        student_id: str,
    ):
        record = db.scalar(
            select(AcademicRecord).where(
                AcademicRecord.student_id == student_id
            )
        )

        if record is None:
            record = AcademicRecord(
                record_id=str(uuid.uuid4()),
                student_id=student_id,
            )

            db.add(record)

        return record

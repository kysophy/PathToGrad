from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import (
    AcademicProgram,
    AcademicRecord,
    ClassGroup,
    StudentProfile,
    User,
)


class StudentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_profile(self, student_id: str) -> StudentProfile | None:
        return self.session.get(StudentProfile, student_id)

    def get_with_policy(self, student_id: str) -> StudentProfile | None:
        return self.session.scalar(
            select(StudentProfile)
            .options(
                joinedload(StudentProfile.program).joinedload(
                    AcademicProgram.track
                ),
                joinedload(StudentProfile.program).joinedload(
                    AcademicProgram.faculty
                ),
                joinedload(StudentProfile.curriculum),
                joinedload(StudentProfile.class_group),
                joinedload(StudentProfile.user),
            )
            .where(StudentProfile.student_id == student_id)
        )

    def get_user(self, user_id: str) -> User | None:
        return self.session.get(User, user_id)

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.scalar(
            select(User).where(User.email == email)
        )

    def get_class_group(self, class_id: str) -> ClassGroup | None:
        return self.session.get(ClassGroup, class_id)

    def save_profile(
        self,
        *,
        student_id: str,
        user_id: str,
        program_id: str | None,
        intake_year: int,
        current_semester: int,
        target_credit_load: int,
        spec_code: str | None = None,
        class_id: str | None = None,
        curriculum_id: str | None = None,
    ) -> StudentProfile:
        profile = self.session.get(StudentProfile, student_id)

        if profile is None:
            profile = StudentProfile(
                student_id=student_id,
                user_id=user_id,
                program_id=program_id,
                intake_year=intake_year,
                current_semester=current_semester,
                target_credit_load=target_credit_load,
                spec_code=spec_code,
                class_id=class_id,
                curriculum_id=curriculum_id,
            )
            self.session.add(profile)
        else:
            profile.user_id = user_id
            profile.program_id = program_id
            profile.intake_year = intake_year
            profile.current_semester = current_semester
            profile.target_credit_load = target_credit_load
            profile.spec_code = spec_code
            profile.class_id = class_id
            profile.curriculum_id = curriculum_id

        self.session.flush()
        return profile

    def ensure_academic_record(self, student_id: str) -> AcademicRecord:
        record = self.session.scalar(
            select(AcademicRecord).where(
                AcademicRecord.student_id == student_id
            )
        )

        if record is None:
            record = AcademicRecord(
                record_id=str(uuid4()),
                student_id=student_id,
            )
            self.session.add(record)

        return record

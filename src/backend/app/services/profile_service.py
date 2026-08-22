from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.curriculum_repository import CurriculumRepository
from app.repositories.student_repository import StudentRepository
from app.schemas.profile import ProfileResponse, ProfileUpsert


class ProfileService:

    @staticmethod
    def save(
        db: Session,
        student_id: str,
        data: ProfileUpsert,
    ) -> ProfileResponse:

        students = StudentRepository(db)
        curricula = CurriculumRepository(db)

        user = students.get_user(data.user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User does not exist.",
            )

        if user.role != "Student":
            raise HTTPException(
                status_code=403,
                detail="The selected user is not a Student.",
            )

        faculty = curricula.get_faculty(data.faculty_id)

        if faculty is None:
            raise HTTPException(
                status_code=422,
                detail="Faculty does not exist.",
            )

        track = curricula.get_track(data.track_id)

        if track is None:
            raise HTTPException(
                status_code=422,
                detail="Program track does not exist.",
            )

        program = curricula.get_program(data.program_id)

        if program is None:
            raise HTTPException(
                status_code=422,
                detail="Academic program does not exist.",
            )

        if program.faculty_id != data.faculty_id:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Academic program does not belong "
                    "to the selected faculty."
                ),
            )

        if program.track_id != data.track_id:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Academic program does not belong "
                    "to the selected program track."
                ),
            )

        if data.class_id is not None:
            class_group = students.get_class_group(data.class_id)
            if class_group is None:
                raise HTTPException(
                    status_code=422,
                    detail="Class group does not exist.",
                )

        curriculum = curricula.get_by_program(data.program_id)

        students.save_profile(
            student_id=student_id,
            user_id=data.user_id,
            program_id=data.program_id,
            intake_year=data.intake_year,
            current_semester=data.current_semester,
            target_credit_load=data.target_credit_load,
            spec_code=data.spec_code,
            class_id=data.class_id,
            curriculum_id=(
                curriculum.curriculum_id if curriculum else None
            ),
        )

        students.ensure_academic_record(student_id)

        db.commit()

        warning = None

        if curriculum is None:
            warning = (
                "No applicable curriculum was found for "
                "the selected program. "
                "The profile is saved but remains incomplete "
                "for planning."
            )

        return ProfileResponse(
            student_id=student_id,
            user_id=data.user_id,
            intake_year=data.intake_year,
            current_semester=data.current_semester,
            target_credit_load=data.target_credit_load,
            program_id=data.program_id,
            spec_code=data.spec_code,
            class_id=data.class_id,
            curriculum_id=(
                curriculum.curriculum_id if curriculum else None
            ),
            faculty_id=faculty.faculty_id,
            faculty_name=faculty.name,
            track_id=track.track_id,
            track_name=track.name,
            program_name=program.name,
            curriculum_version=(
                curriculum.version if curriculum else None
            ),
            is_complete=curriculum is not None,
            warning=warning,
        )

    @staticmethod
    def get(
        db: Session,
        student_id: str,
    ) -> ProfileResponse:

        profile = StudentRepository(db).get_with_policy(student_id)

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Student profile does not exist.",
            )

        program = profile.program
        faculty = program.faculty if program else None
        track = program.track if program else None
        curriculum = profile.curriculum

        warning = None

        if curriculum is None:
            warning = (
                "No applicable curriculum was found "
                "for this profile."
            )

        return ProfileResponse(
            student_id=profile.student_id,
            user_id=profile.user_id,
            intake_year=profile.intake_year,
            current_semester=profile.current_semester,
            target_credit_load=profile.target_credit_load,
            program_id=profile.program_id,
            spec_code=profile.spec_code,
            class_id=profile.class_id,
            curriculum_id=profile.curriculum_id,
            faculty_id=faculty.faculty_id if faculty else None,
            faculty_name=faculty.name if faculty else None,
            track_id=track.track_id if track else None,
            track_name=track.name if track else None,
            program_name=program.name if program else None,
            curriculum_version=(
                curriculum.version if curriculum else None
            ),
            is_complete=curriculum is not None,
            warning=warning,
        )

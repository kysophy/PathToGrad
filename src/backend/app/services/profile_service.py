from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileResponse, ProfileUpsert


class ProfileService:

    @staticmethod
    def save(
        db: Session,
        student_id: str,
        data: ProfileUpsert,
    ) -> ProfileResponse:

        user = ProfileRepository.get_user(
            db,
            data.user_id,
        )

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

        faculty = ProfileRepository.get_faculty(
            db,
            data.faculty_id,
        )

        if faculty is None:
            raise HTTPException(
                status_code=422,
                detail="Faculty does not exist.",
            )

        track = ProfileRepository.get_track(
            db,
            data.track_id,
        )

        if track is None:
            raise HTTPException(
                status_code=422,
                detail="Program track does not exist.",
            )

        program = ProfileRepository.get_program(
            db,
            data.program_id,
        )

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

        curriculum = ProfileRepository.find_curriculum(
            db,
            data.program_id,
            data.intake_year,
        )

        ProfileRepository.save_profile(
            db,
            student_id=student_id,
            user_id=data.user_id,
            program_id=data.program_id,
            intake_year=data.intake_year,
            current_semester=data.current_semester,
            target_credit_load=data.target_credit_load,
        )

        ProfileRepository.ensure_academic_record(
            db,
            student_id,
        )

        db.commit()

        warning = None

        if curriculum is None:
            warning = (
                "No applicable curriculum was found for "
                "the selected program and intake year. "
                "The profile is saved but remains incomplete "
                "for planning."
            )

        return ProfileResponse(
            student_id=student_id,
            user_id=data.user_id,

            faculty_id=faculty.faculty_id,
            faculty_name=faculty.name,

            track_id=track.track_id,
            track_name=track.name,

            program_id=program.program_id,
            program_name=program.name,

            intake_year=data.intake_year,
            current_semester=data.current_semester,
            target_credit_load=data.target_credit_load,

            curriculum_id=(
                curriculum.curriculum_id
                if curriculum
                else None
            ),

            curriculum_version=(
                curriculum.version
                if curriculum
                else None
            ),

            is_complete=curriculum is not None,
            warning=warning,
        )


    @staticmethod
    def get(
        db: Session,
        student_id: str,
    ) -> ProfileResponse:

        profile = ProfileRepository.get_profile(
            db,
            student_id,
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Student profile does not exist.",
            )

        program = ProfileRepository.get_program(
            db,
            profile.program_id,
        )

        faculty = ProfileRepository.get_faculty(
            db,
            program.faculty_id,
        )

        track = ProfileRepository.get_track(
            db,
            program.track_id,
        )

        curriculum = ProfileRepository.find_curriculum(
            db,
            profile.program_id,
            profile.intake_year,
        )

        warning = None

        if curriculum is None:
            warning = (
                "No applicable curriculum was found "
                "for this profile."
            )

        return ProfileResponse(
            student_id=profile.student_id,
            user_id=profile.user_id,

            faculty_id=faculty.faculty_id,
            faculty_name=faculty.name,

            track_id=track.track_id,
            track_name=track.name,

            program_id=program.program_id,
            program_name=program.name,

            intake_year=profile.intake_year,
            current_semester=profile.current_semester,
            target_credit_load=profile.target_credit_load,

            curriculum_id=(
                curriculum.curriculum_id
                if curriculum
                else None
            ),

            curriculum_version=(
                curriculum.version
                if curriculum
                else None
            ),

            is_complete=curriculum is not None,
            warning=warning,
        )


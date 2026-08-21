from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.deterministic.graduation_progress import (
    CompletedCourse,
    calculate_graduation_progress,
)

from app.deterministic.prerequisite_checker import (
    AttemptSnapshot,
    combine_prerequisites,
    evaluate_attempts,
)

from app.repositories.academic_planning_repository import (
    AcademicPlanningRepository,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.schemas.academic_planning import (
    CourseEligibilityResponse,
    GraduationProgressResponse,
    MeetingResponse,
    PrerequisiteCheckResponse,
    PrerequisiteItemResponse,
    SectionResponse,
)


class AcademicPlanningService:

    @staticmethod
    def get_graduation_progress(
        db: Session,
        student_id: str,
    ) -> GraduationProgressResponse:

        profile = ProfileRepository.get_profile(
            db,
            student_id,
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Student profile does not exist."
                ),
            )

        curriculum = (
            ProfileRepository.find_curriculum(
                db,
                profile.program_id,
                profile.intake_year,
            )
        )

        if curriculum is None:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No applicable curriculum can "
                    "be verified for this "
                    "student profile."
                ),
            )

        record = (
            AcademicPlanningRepository.get_record(
                db,
                student_id,
            )
        )

        if record is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Academic record does not exist."
                ),
            )

        passed_rows = (
            AcademicPlanningRepository
            .get_verified_passed_courses(
                db,
                record.record_id,
            )
        )

        required_rows = (
            AcademicPlanningRepository
            .get_required_core_courses(
                db,
                curriculum.curriculum_id,
            )
        )

        completed_courses = [
            CompletedCourse(
                course_code=row.course_code,
                credits=row.credits,
            )
            for row in passed_rows
        ]

        required_course_codes = [
            row.course_code
            for row in required_rows
        ]

        result = (
            calculate_graduation_progress(
                completed_courses=(
                    completed_courses
                ),
                required_credits=(
                    curriculum.required_credits
                ),
                required_course_codes=(
                    required_course_codes
                ),
            )
        )

        return GraduationProgressResponse(
            student_id=student_id,

            curriculum_id=(
                curriculum.curriculum_id
            ),

            required_credits=(
                result.required_credits
            ),

            earned_credits=(
                result.earned_credits
            ),

            remaining_credits=(
                result.remaining_credits
            ),

            credit_requirement_met=(
                result.credit_requirement_met
            ),

            completed_required_courses=(
                result.completed_required_courses
            ),

            missing_required_courses=(
                result.missing_required_courses
            ),

            completed=(
                result.completed
            ),

            progress_percentage=(
                result.progress_percentage
            ),
        )


    @staticmethod
    def check_prerequisites(
        db: Session,
        student_id: str,
        course_code: str,
    ) -> PrerequisiteCheckResponse:

        course = (
            AcademicPlanningRepository
            .get_course_by_code(
                db,
                course_code,
            )
        )

        if course is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Course {course_code} "
                    "does not exist."
                ),
            )

        record = (
            AcademicPlanningRepository
            .get_record(
                db,
                student_id,
            )
        )

        if record is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Academic record does not exist."
                ),
            )

        prerequisite_rows = (
            AcademicPlanningRepository
            .get_prerequisite_courses(
                db,
                course.course_id,
            )
        )

        if not prerequisite_rows:
            return PrerequisiteCheckResponse(
                course_code=course_code,

                eligible=True,

                prerequisites=[],

                warnings=[],
            )

        items: list[
            PrerequisiteItemResponse
        ] = []

        evaluations = []

        warnings: list[str] = []

        for row in prerequisite_rows:

            attempts = (
                AcademicPlanningRepository
                .get_attempts_for_course(
                    db,
                    record.record_id,
                    row.course_id,
                )
            )

            evaluation = evaluate_attempts(
                AttemptSnapshot(
                    attempt_number=(
                        attempt.attempt_number
                    ),

                    result_status=(
                        attempt.result_status
                    ),

                    grade=(
                        float(attempt.grade)
                        if attempt.grade
                        is not None
                        else None
                    ),
                )
                for attempt in attempts
            )

            evaluations.append(
                evaluation
            )

            item_warning = (
                evaluation.warning
            )

            if item_warning:
                warnings.append(
                    f"{row.course_code}: "
                    f"{item_warning}"
                )

            items.append(
                PrerequisiteItemResponse(
                    course_code=(
                        row.course_code
                    ),

                    course_name=(
                        row.course_name
                    ),

                    status=(
                        evaluation.status
                    ),

                    satisfied=(
                        evaluation.satisfied
                    ),

                    warning=(
                        item_warning
                    ),
                )
            )

        eligible = combine_prerequisites(
            evaluations
        )

        return PrerequisiteCheckResponse(
            course_code=course_code,

            eligible=eligible,

            prerequisites=items,

            warnings=warnings,
        )


    @staticmethod
    def get_course_eligibility(
        db: Session,
        student_id: str,
        course_code: str,
        term_id: str,
    ) -> CourseEligibilityResponse:

        prerequisite_result = (
            AcademicPlanningService
            .check_prerequisites(
                db,
                student_id,
                course_code,
            )
        )

        course = (
            AcademicPlanningRepository
            .get_course_by_code(
                db,
                course_code,
            )
        )

        term = (
            AcademicPlanningRepository
            .get_term(
                db,
                term_id,
            )
        )

        if term is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Academic term "
                    f"{term_id} "
                    f"does not exist."
                ),
            )

        offering = (
            AcademicPlanningRepository
            .get_active_offering(
                db,
                course.course_id,
                term_id,
            )
        )

        sections: list[
            SectionResponse
        ] = []

        if offering is not None:

            section_rows = (
                AcademicPlanningRepository
                .get_active_sections(
                    db,
                    offering.offering_id,
                )
            )

            for section in section_rows:

                meeting_rows = (
                    AcademicPlanningRepository
                    .get_meetings(
                        db,
                        section.section_id,
                    )
                )

                meetings = [
                    MeetingResponse(
                        day_of_week=(
                            meeting.day_of_week
                        ),

                        start_time=(
                            meeting.start_time
                            .strftime("%H:%M")
                        ),

                        end_time=(
                            meeting.end_time
                            .strftime("%H:%M")
                        ),
                    )
                    for meeting
                    in meeting_rows
                ]

                sections.append(
                    SectionResponse(
                        section_id=(
                            section.section_id
                        ),

                        section_code=(
                            section.section_code
                        ),

                        capacity=(
                            section.capacity
                        ),

                        meetings=meetings,
                    )
                )

        offered = (
            offering is not None
        )

        if (
            prerequisite_result.eligible
            is None
        ):
            eligible: bool | None = None

        else:
            eligible = (
                prerequisite_result.eligible
                and offered
            )

        return CourseEligibilityResponse(
            course_code=course_code,

            term_id=term_id,

            prerequisite_eligible=(
                prerequisite_result.eligible
            ),

            offered=offered,

            eligible=eligible,

            sections=sections,

            warnings=(
                prerequisite_result.warnings
            ),
        )
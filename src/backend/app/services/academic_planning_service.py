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
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.curriculum_repository import CurriculumRepository
from app.repositories.offering_repository import OfferingRepository
from app.repositories.student_repository import StudentRepository
from app.schemas.academic_planning import (
    CourseEligibilityResponse,
    MeetingResponse,
    PrerequisiteCheckResponse,
    PrerequisiteItemResponse,
    SectionResponse,
)
from app.schemas.tools import GraduationProgress


class AcademicPlanningService:

    @staticmethod
    def get_graduation_progress(
        db: Session,
        student_id: str,
    ) -> GraduationProgress:

        profile = StudentRepository(db).get_with_policy(student_id)

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail="Student profile does not exist.",
            )

        curriculum = profile.curriculum

        if curriculum is None:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No applicable curriculum can "
                    "be verified for this "
                    "student profile."
                ),
            )

        attempts = AttemptRepository(db)
        record = attempts.get_record(student_id)

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Academic record does not exist.",
            )

        passed_rows = attempts.get_verified_passed_courses(record.record_id)

        required_courses = CurriculumRepository(db).list_mandatory_courses(
            curriculum.curriculum_id,
            profile.spec_code,
        )

        completed_courses = [
            CompletedCourse(
                course_code=row.course_code,
                credits=row.credits,
            )
            for row in passed_rows
        ]

        required_course_codes = [
            course.course_code for course in required_courses
        ]

        result = calculate_graduation_progress(
            completed_courses=completed_courses,
            required_credits=curriculum.required_credits,
            required_course_codes=required_course_codes,
        )

        return GraduationProgress(
            student_id=student_id,
            earned_credits=result.earned_credits,
            required_credits=result.required_credits,
            remaining_credits=result.remaining_credits,
            mandatory_passed=len(result.missing_required_courses) == 0,
            credit_requirement_met=result.credit_requirement_met,
            missing_required_courses=result.missing_required_courses,
            gpa=None,
            completed=result.completed,
        )

    @staticmethod
    def check_prerequisites(
        db: Session,
        student_id: str,
        course_code: str,
    ) -> PrerequisiteCheckResponse:

        courses = CourseRepository(db)
        attempts_repo = AttemptRepository(db)

        course = courses.get_by_code(course_code)

        if course is None:
            raise HTTPException(
                status_code=404,
                detail=f"Course {course_code} does not exist.",
            )

        record = attempts_repo.get_record(student_id)

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Academic record does not exist.",
            )

        prerequisite_courses = courses.get_prerequisites(course.course_id)

        if not prerequisite_courses:
            return PrerequisiteCheckResponse(
                course_code=course_code,
                eligible=True,
                prerequisites=[],
                warnings=[],
            )

        items: list[PrerequisiteItemResponse] = []
        evaluations = []
        warnings: list[str] = []

        for required in prerequisite_courses:
            attempts = attempts_repo.list_for_course(
                record.record_id,
                required.course_id,
            )

            evaluation = evaluate_attempts(
                AttemptSnapshot(
                    attempt_number=attempt.attempt_number,
                    result_status=attempt.result_status,
                    grade=(
                        float(attempt.grade)
                        if attempt.grade is not None
                        else None
                    ),
                )
                for attempt in attempts
            )

            evaluations.append(evaluation)

            item_warning = evaluation.warning

            if item_warning:
                warnings.append(f"{required.course_code}: {item_warning}")

            items.append(
                PrerequisiteItemResponse(
                    course_code=required.course_code,
                    name_vi=required.name_vi,
                    name_en=required.name_en,
                    status=evaluation.status,
                    satisfied=evaluation.satisfied,
                    warning=item_warning,
                )
            )

        eligible = combine_prerequisites(evaluations)

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

        prerequisite_result = AcademicPlanningService.check_prerequisites(
            db,
            student_id,
            course_code,
        )

        courses = CourseRepository(db)
        offerings = OfferingRepository(db)

        course = courses.get_by_code(course_code)
        term = offerings.get_term(term_id)

        if term is None:
            raise HTTPException(
                status_code=404,
                detail=f"Academic term {term_id} does not exist.",
            )

        offering = offerings.get_active_offering(course.course_id, term_id)

        sections: list[SectionResponse] = []

        if offering is not None:
            for section in offerings.list_sections_with_meetings(
                offering.offering_id
            ):
                meetings = [
                    MeetingResponse(
                        meeting_type=meeting.meeting_type,
                        day_of_week=meeting.day_of_week,
                        start_time=meeting.start_time.strftime("%H:%M"),
                        end_time=meeting.end_time.strftime("%H:%M"),
                        room=meeting.room,
                    )
                    for meeting in section.meetings
                ]

                sections.append(
                    SectionResponse(
                        section_id=section.section_id,
                        section_code=section.section_code,
                        capacity=section.capacity,
                        meetings=meetings,
                    )
                )

        offered = offering is not None
        warnings = list(prerequisite_result.warnings)

        if offering is not None and len(sections) == 0:
            warnings.append(
                "The course is offered, but no active class-section data is available."
            )

        if prerequisite_result.eligible is None:
            eligible: bool | None = None
        else:
            eligible = prerequisite_result.eligible and offered

        return CourseEligibilityResponse(
            course_code=course_code,
            term_id=term_id,
            prerequisite_eligible=prerequisite_result.eligible,
            offered=offered,
            eligible=eligible,
            sections=sections,
            warnings=warnings,
        )

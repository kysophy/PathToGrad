from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.deterministic.ports import PlanningRepos
from app.deterministic.prerequisites import (
    check_prerequisites as engine_check_prerequisites,
)
from app.deterministic.progress import get_graduation_progress as engine_graduation_progress
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


def _repos(db: Session) -> PlanningRepos:
    return PlanningRepos(
        students=StudentRepository(db),
        courses=CourseRepository(db),
        curriculum=CurriculumRepository(db),
        attempts=AttemptRepository(db),
        offerings=OfferingRepository(db),
    )


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

        repos = _repos(db)
        return engine_graduation_progress(student_id, repos=repos)

    @staticmethod
    def check_prerequisites(
        db: Session,
        student_id: str,
        course_code: str,
    ) -> PrerequisiteCheckResponse:

        courses = CourseRepository(db)
        course = courses.get_by_code(course_code)

        if course is None:
            raise HTTPException(
                status_code=404,
                detail=f"Course {course_code} does not exist.",
            )

        if AttemptRepository(db).get_record(student_id) is None:
            raise HTTPException(
                status_code=404,
                detail="Academic record does not exist.",
            )

        engine_result = engine_check_prerequisites(
            student_id,
            [course.course_id],
            repos=_repos(db),
        )[0]

        items: list[PrerequisiteItemResponse] = []
        for required in engine_result.prerequisites:
            row = courses.get_by_id(required.course_id)
            items.append(
                PrerequisiteItemResponse(
                    course_code=required.course_code,
                    name_vi=row.name_vi if row is not None else required.course_code,
                    name_en=required.name_en,
                    status=required.attempt_status or "Unknown",
                    satisfied=required.satisfied,
                    warning=required.warning,
                )
            )

        return PrerequisiteCheckResponse(
            course_code=course.course_code,
            eligible=engine_result.satisfied,
            prerequisites=items,
            warnings=engine_result.warnings,
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

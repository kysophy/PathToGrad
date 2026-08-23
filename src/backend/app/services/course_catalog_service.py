from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.deterministic.catalog import get_course_catalog as engine_catalog
from app.deterministic.ports import PlanningRepos
from app.deterministic.types import ToolStatus
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.curriculum_repository import CurriculumRepository
from app.repositories.offering_repository import OfferingRepository
from app.repositories.student_repository import StudentRepository
from app.schemas.course_catalog import CourseCatalogItemResponse


def _repos(db: Session) -> PlanningRepos:
    return PlanningRepos(
        students=StudentRepository(db),
        courses=CourseRepository(db),
        curriculum=CurriculumRepository(db),
        attempts=AttemptRepository(db),
        offerings=OfferingRepository(db),
    )


class CourseCatalogService:

    @staticmethod
    def get_catalog(
        db: Session,
        student_id: str,
        term_id: str,
    ) -> list[CourseCatalogItemResponse]:

        if OfferingRepository(db).get_term(term_id) is None:
            raise HTTPException(
                status_code=404,
                detail=f"Academic term {term_id} does not exist.",
            )

        if StudentRepository(db).get_profile(student_id) is None:
            raise HTTPException(
                status_code=404,
                detail="Student profile does not exist.",
            )

        courses = CourseRepository(db)
        result = engine_catalog(student_id, term_id, repos=_repos(db))
        items: list[CourseCatalogItemResponse] = []

        for course in result.courses:
            prereq_codes = [
                required.course_code
                for required in courses.get_prerequisites(course.course_id)
            ]
            prerequisite_eligible: bool | None
            if course.blocked:
                prerequisite_eligible = False
            elif result.status == ToolStatus.UNCERTAIN:
                prerequisite_eligible = None
            else:
                prerequisite_eligible = True

            offered = not course.not_offered
            if prerequisite_eligible is None:
                eligible: bool | None = None
            else:
                eligible = prerequisite_eligible and offered

            items.append(
                CourseCatalogItemResponse(
                    course_code=course.course_code,
                    course_name=course.name_en,
                    name_vi=course.name_vi,
                    name_en=course.name_en,
                    credits=course.credits,
                    assigned_semester=course.assigned_semester,
                    is_mandatory=course.is_mandatory,
                    prerequisite_codes=prereq_codes,
                    prerequisite_eligible=prerequisite_eligible,
                    offered=offered,
                    eligible=eligible,
                    primary_status=course.primary_status,
                    blocked=course.blocked,
                    not_offered=course.not_offered,
                    warnings=[
                        text
                        for text in result.warnings
                        if course.course_code in text
                    ],
                )
            )

        return items

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.course_catalog_repository import (
    CourseCatalogRepository,
)
from app.repositories.offering_repository import OfferingRepository

from app.schemas.course_catalog import (
    CourseCatalogItemResponse,
)

from app.services.academic_planning_service import (
    AcademicPlanningService,
)


class CourseCatalogService:

    @staticmethod
    def get_catalog(
        db: Session,
        student_id: str,
        term_id: str,
    ) -> list[CourseCatalogItemResponse]:

        offerings = OfferingRepository(db)

        term = offerings.get_term(term_id)

        if term is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Academic term "
                    f"{term_id} does not exist."
                ),
            )

        courses = (
            CourseCatalogRepository
            .get_active_courses(
                db
            )
        )

        result: list[
            CourseCatalogItemResponse
        ] = []

        for course in courses:

            prerequisite_result = (
                AcademicPlanningService
                .check_prerequisites(
                    db,
                    student_id,
                    course.course_code,
                )
            )

            offering = offerings.get_active_offering(
                course.course_id,
                term_id,
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

            prerequisite_codes = [
                item.course_code
                for item
                in prerequisite_result.prerequisites
            ]

            result.append(
                CourseCatalogItemResponse(
                    course_code=(
                        course.course_code
                    ),

                    course_name=(
                        course.name_en
                    ),

                    credits=(
                        course.credits
                    ),

                    prerequisite_codes=(
                        prerequisite_codes
                    ),

                    prerequisite_eligible=(
                        prerequisite_result.eligible
                    ),

                    offered=offered,

                    eligible=eligible,

                    warnings=(
                        prerequisite_result.warnings
                    ),
                )
            )

        return result
    
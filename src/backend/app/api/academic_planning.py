from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.academic_planning import (
    CourseEligibilityResponse,
    PrerequisiteCheckResponse,
)
from app.schemas.tools import GraduationProgress

from app.services.academic_planning_service import (
    AcademicPlanningService,
)


router = APIRouter(
    prefix="/api/students",
    tags=["Academic Planning"],
)


@router.get(
    "/{student_id}/graduation-progress",
    response_model=GraduationProgress,
)
def get_graduation_progress(
    student_id: str,
    db: Session = Depends(get_db),
):
    return (
        AcademicPlanningService
        .get_graduation_progress(
            db,
            student_id,
        )
    )


@router.get(
    "/{student_id}/courses/"
    "{course_code}/prerequisites",
    response_model=PrerequisiteCheckResponse,
)
def check_prerequisites(
    student_id: str,
    course_code: str,
    db: Session = Depends(get_db),
):
    return (
        AcademicPlanningService
        .check_prerequisites(
            db,
            student_id,
            course_code,
        )
    )


@router.get(
    "/{student_id}/courses/"
    "{course_code}/eligibility",
    response_model=CourseEligibilityResponse,
)
def get_course_eligibility(
    student_id: str,
    course_code: str,
    term_id: str,
    db: Session = Depends(get_db),
):
    return (
        AcademicPlanningService
        .get_course_eligibility(
            db,
            student_id,
            course_code,
            term_id,
        )
    )
from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.course_catalog import (
    CourseCatalogItemResponse,
)

from app.services.course_catalog_service import (
    CourseCatalogService,
)


router = APIRouter(
    prefix="/api/students",
    tags=["Course Catalog"],
)


@router.get(
    "/{student_id}/course-catalog",
    response_model=list[
        CourseCatalogItemResponse
    ],
)
def get_course_catalog(
    student_id: str,
    term_id: str,
    db: Session = Depends(get_db),
):
    return (
        CourseCatalogService
        .get_catalog(
            db,
            student_id,
            term_id,
        )
    )
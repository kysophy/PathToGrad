
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.academic_record import (
    AcademicRecordResponse,
    CourseAttemptCreate,
)
from app.services.academic_record_service import (
    AcademicRecordService,
)


router = APIRouter(
    prefix="/api/students",
    tags=["Academic Record"],
)


@router.get(
    "/{student_id}/academic-record",
    response_model=AcademicRecordResponse,
)
def get_academic_record(
    student_id: str,
    db: Session = Depends(get_db),
):
    return AcademicRecordService.get(
        db,
        student_id,
    )


@router.post(
    "/{student_id}/academic-record/attempts",
    response_model=AcademicRecordResponse,
)
def add_course_attempt(
    student_id: str,
    data: CourseAttemptCreate,
    db: Session = Depends(get_db),
):
    return AcademicRecordService.add_attempt(
        db,
        student_id,
        data,
    )

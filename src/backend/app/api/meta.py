from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.course_repository import CourseRepository
from app.repositories.curriculum_repository import CurriculumRepository
from app.repositories.offering_repository import OfferingRepository


router = APIRouter(
    prefix="/api/meta",
    tags=["Academic Metadata"],
)


@router.get("/faculties")
def get_faculties(
    db: Session = Depends(get_db),
):
    rows = CurriculumRepository(db).list_faculties()
    return [
        {"faculty_id": row.faculty_id, "name": row.name}
        for row in rows
    ]


@router.get("/tracks")
def get_tracks(
    db: Session = Depends(get_db),
):
    rows = CurriculumRepository(db).list_tracks()
    return [
        {
            "track_id": row.track_id,
            "name": row.name,
            "min_credits_per_term": row.min_credits_per_term,
            "max_credits_per_term": row.max_credits_per_term,
            "min_courses": row.min_courses,
            "max_courses": row.max_courses,
        }
        for row in rows
    ]


@router.get("/programs")
def get_programs(
    faculty_id: str,
    track_id: str,
    db: Session = Depends(get_db),
):
    rows = CurriculumRepository(db).list_programs(faculty_id, track_id)
    return [
        {"program_id": row.program_id, "name": row.name}
        for row in rows
    ]


@router.get("/curriculum")
def find_curriculum(
    program_id: str,
    intake_year: int,
    db: Session = Depends(get_db),
):
    curriculum = CurriculumRepository(db).get_by_program(program_id)

    if curriculum is None:
        return {
            "found": False,
            "curriculum_id": None,
            "version": None,
            "intake_year": intake_year,
        }

    return {
        "found": True,
        "curriculum_id": curriculum.curriculum_id,
        "version": curriculum.version,
        "required_credits": curriculum.required_credits,
        "intake_year": intake_year,
    }


@router.get("/courses")
def get_courses(
    db: Session = Depends(get_db),
):
    rows = CourseRepository(db).list_active()
    return [
        {
            "course_code": row.course_code,
            "name_vi": row.name_vi,
            "name_en": row.name_en,
            "credits": row.credits,
        }
        for row in rows
    ]


@router.get("/terms")
def get_terms(
    db: Session = Depends(get_db),
):
    rows = OfferingRepository(db).list_terms()
    return [
        {
            "term_id": row.term_id,
            "name": row.name,
            "term_type": row.term_type,
        }
        for row in rows
    ]

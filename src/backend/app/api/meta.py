from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.academic import (
    AcademicProgram,
    AcademicTerm,
    Course,
    Curriculum,
    CurriculumApplicability,
    Faculty,
    ProgramTrack,
)


router = APIRouter(
    prefix="/api/meta",
    tags=["Academic Metadata"],
)


@router.get("/faculties")
def get_faculties(
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(Faculty).order_by(Faculty.name)
    ).all()

    return [
        {
            "faculty_id": row.faculty_id,
            "name": row.name,
        }
        for row in rows
    ]


@router.get("/tracks")
def get_tracks(
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(ProgramTrack).order_by(
            ProgramTrack.name
        )
    ).all()

    return [
        {
            "track_id": row.track_id,
            "name": row.name,
        }
        for row in rows
    ]


@router.get("/programs")
def get_programs(
    faculty_id: str,
    track_id: str,
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(AcademicProgram)
        .where(
            AcademicProgram.faculty_id == faculty_id,
            AcademicProgram.track_id == track_id,
        )
        .order_by(AcademicProgram.name)
    ).all()

    return [
        {
            "program_id": row.program_id,
            "name": row.name,
        }
        for row in rows
    ]


@router.get("/curriculum")
def find_curriculum(
    program_id: str,
    intake_year: int,
    db: Session = Depends(get_db),
):
    curriculum = db.scalar(
        select(Curriculum)
        .join(
            CurriculumApplicability,
            Curriculum.curriculum_id
            == CurriculumApplicability.curriculum_id,
        )
        .where(
            Curriculum.program_id == program_id,
            CurriculumApplicability.intake_year
            == intake_year,
        )
    )

    if curriculum is None:
        return {
            "found": False,
            "curriculum_id": None,
            "version": None,
        }

    return {
        "found": True,
        "curriculum_id": curriculum.curriculum_id,
        "version": curriculum.version,
    }


@router.get("/courses")
def get_courses(
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(Course)
        .where(Course.status == "Active")
        .order_by(Course.course_code)
    ).all()

    return [
        {
            "course_code": row.course_code,
            "course_name": row.course_name,
            "credits": row.credits,
        }
        for row in rows
    ]


@router.get("/terms")
def get_terms(
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(AcademicTerm)
        .order_by(AcademicTerm.name)
    ).all()

    return [
        {
            "term_id": row.term_id,
            "name": row.name,
        }
        for row in rows
    ]

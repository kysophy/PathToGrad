from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.profile import ProfileResponse, ProfileUpsert
from app.services.profile_service import ProfileService


router = APIRouter(
    prefix="/api/students",
    tags=["Student Profile"],
)


@router.get(
    "/{student_id}/profile",
    response_model=ProfileResponse,
)
def get_profile(
    student_id: str,
    db: Session = Depends(get_db),
):
    return ProfileService.get(
        db,
        student_id,
    )


@router.put(
    "/{student_id}/profile",
    response_model=ProfileResponse,
)
def save_profile(
    student_id: str,
    data: ProfileUpsert,
    db: Session = Depends(get_db),
):
    return ProfileService.save(
        db,
        student_id,
        data,
    )

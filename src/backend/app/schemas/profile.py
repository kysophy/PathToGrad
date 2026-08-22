from pydantic import BaseModel, Field

from app.schemas.academic import StudentProfileRead


class ProfileUpsert(BaseModel):
    user_id: str

    faculty_id: str
    track_id: str
    program_id: str

    intake_year: int = Field(gt=1900)
    current_semester: int = Field(gt=0)

    target_credit_load: int = Field(gt=0)

    spec_code: str | None = None
    class_id: str | None = None


class ProfileResponse(StudentProfileRead):
    faculty_id: str | None = None
    faculty_name: str | None = None

    track_id: str | None = None
    track_name: str | None = None

    program_name: str | None = None

    curriculum_version: str | None = None

    is_complete: bool
    warning: str | None = None

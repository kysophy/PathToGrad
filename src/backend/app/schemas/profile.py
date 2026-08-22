from pydantic import BaseModel, Field

class ProfileUpsert(BaseModel):
    user_id: str

    faculty_id: str
    track_id: str
    program_id: str

    intake_year: int = Field(gt=1900)
    current_semester: int = Field(gt=0)

    target_credit_load: int = Field(
        ge=14,
        le=24,
    )


class ProfileResponse(BaseModel):
    student_id: str
    user_id: str

    faculty_id: str
    faculty_name: str

    track_id: str
    track_name: str

    program_id: str
    program_name: str

    intake_year: int
    current_semester: int
    target_credit_load: int

    curriculum_id: str | None
    curriculum_version: str | None

    is_complete: bool
    warning: str | None = None

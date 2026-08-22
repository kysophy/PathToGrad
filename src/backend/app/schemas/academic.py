from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import AccountStatus, ResultStatus, UserRole


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    full_name: str
    email: str
    role: UserRole
    account_status: AccountStatus


class ClassGroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    class_id: str
    class_code: str
    program_id: str
    intake_year: int
    advisor_user_id: str


class StudentProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
    user_id: str
    intake_year: int
    current_semester: int
    target_credit_load: int
    program_id: str | None
    spec_code: str | None
    class_id: str | None
    curriculum_id: str | None


class AcademicRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    record_id: str
    student_id: str
    updated_at: datetime


class CourseAttemptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attempt_id: str
    record_id: str
    course_id: str
    term_id: str
    attempt_number: int = Field(ge=1, le=2)
    grade: Decimal | None
    result_status: ResultStatus
    credits_earned: int

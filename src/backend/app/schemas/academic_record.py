from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.schemas.enums import ResultStatus


class CourseAttemptCreate(BaseModel):
    course_code: str
    term_id: str

    attempt_number: int = Field(ge=1, le=2)

    grade: float | None = None

    result_status: ResultStatus

    credits_earned: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_attempt(self):
        if (
            self.result_status
            in {
                ResultStatus.PASSED,
                ResultStatus.FAILED,
            }
            and self.grade is None
        ):
            raise ValueError(
                "Grade is required for Passed or Failed attempts."
            )

        if (
            self.result_status
            in {
                ResultStatus.FAILED,
                ResultStatus.IN_PROGRESS,
            }
            and self.credits_earned != 0
        ):
            raise ValueError(
                "Failed or InProgress attempts "
                "must have 0 earned credits."
            )

        return self


class CourseAttemptResponse(BaseModel):
    attempt_id: str

    course_code: str
    name_vi: str
    name_en: str

    term_id: str
    term_name: str

    attempt_number: int

    grade: float | None

    result_status: ResultStatus

    credits_earned: int


class AcademicRecordResponse(BaseModel):
    record_id: str
    student_id: str
    updated_at: datetime

    earned_credits: int
    passed_courses: list[str]

    attempts: list[CourseAttemptResponse]

from pydantic import BaseModel


class GraduationProgressResponse(BaseModel):
    student_id: str
    curriculum_id: str

    required_credits: int
    earned_credits: int
    remaining_credits: int

    credit_requirement_met: bool

    completed_required_courses: list[str]
    missing_required_courses: list[str]

    completed: bool
    progress_percentage: float


class PrerequisiteItemResponse(BaseModel):
    course_code: str
    course_name: str

    status: str
    satisfied: bool | None

    warning: str | None = None


class PrerequisiteCheckResponse(BaseModel):
    course_code: str

    eligible: bool | None

    prerequisites: list[PrerequisiteItemResponse]

    warnings: list[str]


class MeetingResponse(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str


class SectionResponse(BaseModel):
    section_id: str
    section_code: str

    capacity: int

    meetings: list[MeetingResponse]


class CourseEligibilityResponse(BaseModel):
    course_code: str
    term_id: str

    prerequisite_eligible: bool | None

    offered: bool

    eligible: bool | None

    sections: list[SectionResponse]

    warnings: list[str]
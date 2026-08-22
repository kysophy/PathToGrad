from pydantic import BaseModel


class PrerequisiteItemResponse(BaseModel):
    course_code: str
    name_vi: str
    name_en: str

    status: str
    satisfied: bool | None

    warning: str | None = None


class PrerequisiteCheckResponse(BaseModel):
    course_code: str

    eligible: bool | None

    prerequisites: list[PrerequisiteItemResponse]

    warnings: list[str]


class MeetingResponse(BaseModel):
    meeting_type: str
    day_of_week: str
    start_time: str
    end_time: str
    room: str


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

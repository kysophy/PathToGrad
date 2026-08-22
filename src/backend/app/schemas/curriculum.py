from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import (
    CourseStatus,
    DayOfWeek,
    MeetingType,
    OfferingStatus,
    RequirementType,
    SectionStatus,
    TermType,
)


class FacultyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    faculty_id: str
    name: str


class ProgramTrackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    track_id: str
    name: str
    min_credits_per_term: int
    max_credits_per_term: int
    min_courses: int
    max_courses: int


class AcademicProgramRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    program_id: str
    faculty_id: str
    track_id: str
    name: str


class CurriculumRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    curriculum_id: str
    program_id: str
    version: str
    required_credits: int


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    course_id: str
    course_code: str
    name_vi: str
    name_en: str
    credits: int
    status: CourseStatus


class CurriculumCourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    curr_course_id: str
    curriculum_id: str
    course_id: str
    requirement_type: RequirementType
    assigned_semester: int = Field(gt=0)
    spec_code: str | None


class PrerequisiteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    prereq_id: int
    course_id: str
    required_course_id: str


class AcademicTermRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    term_id: str
    name: str
    start_date: date
    end_date: date
    term_type: TermType


class CourseOfferingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    offering_id: str
    course_id: str
    term_id: str
    status: OfferingStatus


class ClassSectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    section_id: str
    offering_id: str
    section_code: str
    capacity: int
    status: SectionStatus


class SectionMeetingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    meeting_id: str
    section_id: str
    meeting_type: MeetingType
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    room: str
    instructor: str | None

from datetime import datetime, time
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    Time,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[str] = mapped_column(
        Enum("Student", "Advisor", "Admin"),
        nullable=False,
    )

    account_status: Mapped[str] = mapped_column(
        Enum("Active", "Suspended"),
        nullable=False,
    )


class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class ProgramTrack(Base):
    __tablename__ = "program_track"

    track_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class AcademicProgram(Base):
    __tablename__ = "academic_program"

    program_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    faculty_id: Mapped[str] = mapped_column(
        ForeignKey("faculty.faculty_id"),
        nullable=False,
    )

    track_id: Mapped[str] = mapped_column(
        ForeignKey("program_track.track_id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Curriculum(Base):
    __tablename__ = "curriculum"

    curriculum_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    program_id: Mapped[str] = mapped_column(
        ForeignKey("academic_program.program_id"),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(String(50), nullable=False)
    required_credits: Mapped[int] = mapped_column(Integer, nullable=False)


class CurriculumApplicability(Base):
    __tablename__ = "curriculum_applicability"

    curriculum_id: Mapped[str] = mapped_column(
        ForeignKey("curriculum.curriculum_id"),
        primary_key=True,
    )

    intake_year: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )


class StudentProfile(Base):
    __tablename__ = "student_profile"

    student_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        unique=True,
    )

    intake_year: Mapped[int] = mapped_column(Integer, nullable=False)
    current_semester: Mapped[int] = mapped_column(Integer, nullable=False)
    target_credit_load: Mapped[int] = mapped_column(Integer, nullable=False)

    program_id: Mapped[str | None] = mapped_column(
        ForeignKey("academic_program.program_id"),
        nullable=True,
    )


class Course(Base):
    __tablename__ = "course"

    course_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    course_code: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        unique=True,
    )

    course_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    credits: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(
        Enum("Active", "Archived"),
        nullable=False,
        default="Active",
    )


class AcademicTerm(Base):
    __tablename__ = "academic_term"

    term_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    start_date = mapped_column(Date, nullable=False)
    end_date = mapped_column(Date, nullable=False)


class AcademicRecord(Base):
    __tablename__ = "academic_record"

    record_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    student_id: Mapped[str] = mapped_column(
        ForeignKey("student_profile.student_id"),
        nullable=False,
        unique=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


class CourseAttempt(Base):
    __tablename__ = "course_attempt"

    __table_args__ = (
        UniqueConstraint(
            "record_id",
            "course_id",
            "attempt_number",
            name="uq_course_attempt",
        ),
    )

    attempt_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    record_id: Mapped[str] = mapped_column(
        ForeignKey("academic_record.record_id"),
        nullable=False,
    )

    course_id: Mapped[str] = mapped_column(
        ForeignKey("course.course_id"),
        nullable=False,
    )

    term_id: Mapped[str] = mapped_column(
        ForeignKey("academic_term.term_id"),
        nullable=False,
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    grade: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1),
        nullable=True,
    )

    result_status: Mapped[str] = mapped_column(
        Enum("Passed", "Failed", "InProgress"),
        nullable=False,
    )

    credits_earned: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

class CurriculumCourse(Base):
    __tablename__ = "curriculum_course"

    __table_args__ = (
        UniqueConstraint(
            "curriculum_id",
            "course_id",
            name="uq_curriculum_course",
        ),
    )

    curr_course_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    curriculum_id: Mapped[str] = mapped_column(
        ForeignKey("curriculum.curriculum_id"),
        nullable=False,
    )

    course_id: Mapped[str] = mapped_column(
        ForeignKey("course.course_id"),
        nullable=False,
    )

    requirement_type: Mapped[str] = mapped_column(
        Enum("Core", "Elective"),
        nullable=False,
    )


class Prerequisite(Base):
    __tablename__ = "prerequisite"

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "required_course_id",
            name="uq_prerequisite_rule",
        ),
    )

    prereq_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    course_id: Mapped[str] = mapped_column(
        ForeignKey("course.course_id"),
        nullable=False,
    )

    required_course_id: Mapped[str] = mapped_column(
        ForeignKey("course.course_id"),
        nullable=False,
    )


class CourseOffering(Base):
    __tablename__ = "course_offering"

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "term_id",
            name="uq_course_offering",
        ),
    )

    offering_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    course_id: Mapped[str] = mapped_column(
        ForeignKey("course.course_id"),
        nullable=False,
    )

    term_id: Mapped[str] = mapped_column(
        ForeignKey("academic_term.term_id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "Active",
            "Inactive",
            "Archived",
        ),
        nullable=False,
        default="Active",
    )


class ClassSection(Base):
    __tablename__ = "class_section"

    __table_args__ = (
        UniqueConstraint(
            "offering_id",
            "section_code",
            name="uq_section_code_per_offering",
        ),
    )

    section_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    offering_id: Mapped[str] = mapped_column(
        ForeignKey("course_offering.offering_id"),
        nullable=False,
    )

    section_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "Active",
            "Inactive",
            "Archived",
        ),
        nullable=False,
        default="Active",
    )


class SectionMeeting(Base):
    __tablename__ = "section_meeting"

    meeting_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    section_id: Mapped[str] = mapped_column(
        ForeignKey("class_section.section_id"),
        nullable=False,
    )

    day_of_week: Mapped[str] = mapped_column(
        Enum(
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ),
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )
from __future__ import annotations

from datetime import date, time

from sqlalchemy import (
    CheckConstraint,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.schemas.enums import (
    CourseStatus,
    DayOfWeek,
    MeetingType,
    OfferingStatus,
    RequirementType,
    SectionStatus,
    TermType,
)

_enum_values = lambda cls: [item.value for item in cls]


class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    programs: Mapped[list[AcademicProgram]] = relationship(
        back_populates="faculty"
    )


class ProgramTrack(Base):
    __tablename__ = "program_track"

    __table_args__ = (
        CheckConstraint(
            "min_credits_per_term > 0",
            name="chk_track_min_credits",
        ),
        CheckConstraint(
            "max_credits_per_term >= min_credits_per_term",
            name="chk_track_max_credits",
        ),
        CheckConstraint(
            "min_courses > 0",
            name="chk_track_min_courses",
        ),
        CheckConstraint(
            "max_courses >= min_courses",
            name="chk_track_max_courses",
        ),
    )

    track_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    min_credits_per_term: Mapped[int] = mapped_column(Integer, nullable=False)
    max_credits_per_term: Mapped[int] = mapped_column(Integer, nullable=False)
    min_courses: Mapped[int] = mapped_column(Integer, nullable=False)
    max_courses: Mapped[int] = mapped_column(Integer, nullable=False)

    programs: Mapped[list[AcademicProgram]] = relationship(
        back_populates="track"
    )


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

    faculty: Mapped[Faculty] = relationship(back_populates="programs")
    track: Mapped[ProgramTrack] = relationship(back_populates="programs")
    curricula: Mapped[list[Curriculum]] = relationship(
        back_populates="program"
    )


class Curriculum(Base):
    __tablename__ = "curriculum"

    __table_args__ = (
        CheckConstraint(
            "required_credits > 0",
            name="chk_required_credits",
        ),
        UniqueConstraint(
            "program_id",
            "version",
            name="uq_curriculum_program_version",
        ),
    )

    curriculum_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    program_id: Mapped[str] = mapped_column(
        ForeignKey("academic_program.program_id"),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(String(50), nullable=False)
    required_credits: Mapped[int] = mapped_column(Integer, nullable=False)

    program: Mapped[AcademicProgram] = relationship(back_populates="curricula")
    courses: Mapped[list[CurriculumCourse]] = relationship(
        back_populates="curriculum"
    )


class Course(Base):
    __tablename__ = "course"

    __table_args__ = (
        CheckConstraint("credits > 0", name="chk_course_credits"),
    )

    course_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    course_code: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        unique=True,
    )

    name_vi: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)

    credits: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(
        Enum(*_enum_values(CourseStatus), name="course_status"),
        nullable=False,
        default=CourseStatus.ACTIVE.value,
    )

    curriculum_rows: Mapped[list[CurriculumCourse]] = relationship(
        back_populates="course"
    )
    offerings: Mapped[list[CourseOffering]] = relationship(
        back_populates="course"
    )


class CurriculumCourse(Base):
    __tablename__ = "curriculum_course"

    __table_args__ = (
        UniqueConstraint(
            "curriculum_id",
            "course_id",
            name="uq_curriculum_course",
        ),
        CheckConstraint(
            "assigned_semester > 0",
            name="chk_assigned_semester",
        ),
    )

    curr_course_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    curriculum_id: Mapped[str] = mapped_column(
        ForeignKey("curriculum.curriculum_id"),
        nullable=False,
    )

    course_id: Mapped[str] = mapped_column(
        ForeignKey("course.course_id"),
        nullable=False,
    )

    requirement_type: Mapped[str] = mapped_column(
        Enum(*_enum_values(RequirementType), name="requirement_type"),
        nullable=False,
    )

    assigned_semester: Mapped[int] = mapped_column(Integer, nullable=False)

    spec_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )  # "GEN" for semesters 1–6; a real code (SE, CN, …) from semester 7.

    curriculum: Mapped[Curriculum] = relationship(back_populates="courses")
    course: Mapped[Course] = relationship(back_populates="curriculum_rows")


class Prerequisite(Base):
    __tablename__ = "prerequisite"

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "required_course_id",
            name="uq_prerequisite_rule",
        ),
        CheckConstraint(
            "course_id <> required_course_id",
            name="chk_prerequisite_not_self",
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

    course: Mapped[Course] = relationship(
        foreign_keys=[course_id],
    )
    required_course: Mapped[Course] = relationship(
        foreign_keys=[required_course_id],
    )


class AcademicTerm(Base):
    __tablename__ = "academic_term"

    term_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    term_type: Mapped[str] = mapped_column(
        Enum(*_enum_values(TermType), name="term_type"),
        nullable=False,
    )

    offerings: Mapped[list[CourseOffering]] = relationship(
        back_populates="term"
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

    offering_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    course_id: Mapped[str] = mapped_column(
        ForeignKey("course.course_id"),
        nullable=False,
    )

    term_id: Mapped[str] = mapped_column(
        ForeignKey("academic_term.term_id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        Enum(*_enum_values(OfferingStatus), name="offering_status"),
        nullable=False,
        default=OfferingStatus.ACTIVE.value,
    )

    course: Mapped[Course] = relationship(back_populates="offerings")
    term: Mapped[AcademicTerm] = relationship(back_populates="offerings")
    sections: Mapped[list[ClassSection]] = relationship(
        back_populates="offering"
    )


class ClassSection(Base):
    __tablename__ = "class_section"

    __table_args__ = (
        UniqueConstraint(
            "offering_id",
            "section_code",
            name="uq_section_code_per_offering",
        ),
        CheckConstraint("capacity >= 0", name="chk_section_capacity"),
    )

    section_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    offering_id: Mapped[str] = mapped_column(
        ForeignKey("course_offering.offering_id"),
        nullable=False,
    )

    section_code: Mapped[str] = mapped_column(String(20), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(
        Enum(*_enum_values(SectionStatus), name="section_status"),
        nullable=False,
        default=SectionStatus.ACTIVE.value,
    )

    offering: Mapped[CourseOffering] = relationship(back_populates="sections")
    meetings: Mapped[list[SectionMeeting]] = relationship(
        back_populates="section"
    )


class SectionMeeting(Base):
    __tablename__ = "section_meeting"

    __table_args__ = (
        CheckConstraint(
            "end_time > start_time",
            name="chk_meeting_time",
        ),
    )

    meeting_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    section_id: Mapped[str] = mapped_column(
        ForeignKey("class_section.section_id"),
        nullable=False,
    )

    meeting_type: Mapped[str] = mapped_column(
        Enum(*_enum_values(MeetingType), name="meeting_type"),
        nullable=False,
    )

    day_of_week: Mapped[str] = mapped_column(
        Enum(*_enum_values(DayOfWeek), name="day_of_week"),
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    room: Mapped[str] = mapped_column(String(50), nullable=False)
    instructor: Mapped[str | None] = mapped_column(String(100), nullable=True)

    section: Mapped[ClassSection] = relationship(back_populates="meetings")

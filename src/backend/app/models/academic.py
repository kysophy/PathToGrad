from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.schemas.enums import AccountStatus, ResultStatus, UserRole

_enum_values = lambda cls: [item.value for item in cls]


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[str] = mapped_column(
        Enum(*_enum_values(UserRole), name="user_role"),
        nullable=False,
    )

    account_status: Mapped[str] = mapped_column(
        Enum(*_enum_values(AccountStatus), name="account_status"),
        nullable=False,
    )

    student_profile: Mapped[StudentProfile | None] = relationship(
        back_populates="user"
    )
    advised_classes: Mapped[list[ClassGroup]] = relationship(
        back_populates="advisor"
    )


class ClassGroup(Base):
    __tablename__ = "class_group"

    __table_args__ = (
        CheckConstraint("intake_year > 1900", name="chk_class_intake_year"),
    )

    class_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    class_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    program_id: Mapped[str] = mapped_column(
        ForeignKey("academic_program.program_id"),
        nullable=False,
    )

    intake_year: Mapped[int] = mapped_column(Integer, nullable=False)

    advisor_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
    )

    program: Mapped["AcademicProgram"] = relationship("AcademicProgram")
    advisor: Mapped[User] = relationship(back_populates="advised_classes")
    students: Mapped[list[StudentProfile]] = relationship(
        back_populates="class_group"
    )


class StudentProfile(Base):
    __tablename__ = "student_profile"

    __table_args__ = (
        CheckConstraint("intake_year > 1900", name="chk_intake_year"),
        CheckConstraint(
            "current_semester > 0",
            name="chk_current_semester",
        ),
    )

    student_id: Mapped[str] = mapped_column(String(20), primary_key=True)

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

    spec_code: Mapped[str | None] = mapped_column(String(10), nullable=True)

    class_id: Mapped[str | None] = mapped_column(
        ForeignKey("class_group.class_id"),
        nullable=True,
    )

    curriculum_id: Mapped[str | None] = mapped_column(
        ForeignKey("curriculum.curriculum_id"),
        nullable=True,
    )

    user: Mapped[User] = relationship(back_populates="student_profile")
    program: Mapped["AcademicProgram | None"] = relationship("AcademicProgram")
    class_group: Mapped[ClassGroup | None] = relationship(
        back_populates="students"
    )
    curriculum: Mapped["Curriculum | None"] = relationship("Curriculum")
    academic_record: Mapped[AcademicRecord | None] = relationship(
        back_populates="student"
    )


class AcademicRecord(Base):
    __tablename__ = "academic_record"

    record_id: Mapped[str] = mapped_column(String(36), primary_key=True)

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

    student: Mapped[StudentProfile] = relationship(
        back_populates="academic_record"
    )
    attempts: Mapped[list[CourseAttempt]] = relationship(
        back_populates="record"
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
        CheckConstraint(
            "attempt_number IN (1, 2)",
            name="chk_attempt_number",
        ),
        CheckConstraint(
            "credits_earned >= 0",
            name="chk_credits_earned",
        ),
    )

    attempt_id: Mapped[str] = mapped_column(String(36), primary_key=True)

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

    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)

    grade: Mapped[Decimal | None] = mapped_column(
        Numeric(3, 1),
        nullable=True,
    )

    result_status: Mapped[str] = mapped_column(
        Enum(*_enum_values(ResultStatus), name="result_status"),
        nullable=False,
    )

    credits_earned: Mapped[int] = mapped_column(Integer, nullable=False)

    record: Mapped[AcademicRecord] = relationship(back_populates="attempts")
    course: Mapped["Course"] = relationship("Course")
    term: Mapped["AcademicTerm"] = relationship("AcademicTerm")

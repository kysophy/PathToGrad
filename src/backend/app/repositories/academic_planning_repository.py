from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academic import (
    AcademicRecord,
    AcademicTerm,
    ClassSection,
    Course,
    CourseAttempt,
    CourseOffering,
    CurriculumCourse,
    Prerequisite,
    SectionMeeting,
)


class AcademicPlanningRepository:

    @staticmethod
    def get_record(
        db: Session,
        student_id: str,
    ):
        return db.scalar(
            select(AcademicRecord)
            .where(
                AcademicRecord.student_id
                == student_id
            )
        )


    @staticmethod
    def get_verified_passed_courses(
        db: Session,
        record_id: str,
    ):
        return db.execute(
            select(
                Course.course_code,
                Course.credits,
            )
            .join(
                CourseAttempt,
                CourseAttempt.course_id
                == Course.course_id,
            )
            .where(
                CourseAttempt.record_id
                == record_id,

                CourseAttempt.result_status
                == "Passed",

                CourseAttempt.grade.is_not(
                    None
                ),
            )
            .distinct()
            .order_by(
                Course.course_code
            )
        ).all()


    @staticmethod
    def get_required_core_courses(
        db: Session,
        curriculum_id: str,
    ):
        return db.execute(
            select(
                Course.course_code,
                Course.course_name,
                Course.credits,
            )
            .join(
                CurriculumCourse,
                CurriculumCourse.course_id
                == Course.course_id,
            )
            .where(
                CurriculumCourse.curriculum_id
                == curriculum_id,

                CurriculumCourse.requirement_type
                == "Core",
            )
            .order_by(
                Course.course_code
            )
        ).all()


    @staticmethod
    def get_course_by_code(
        db: Session,
        course_code: str,
    ):
        return db.scalar(
            select(Course)
            .where(
                Course.course_code
                == course_code
            )
        )


    @staticmethod
    def get_prerequisite_courses(
        db: Session,
        course_id: str,
    ):
        return db.execute(
            select(
                Course.course_id,
                Course.course_code,
                Course.course_name,
            )
            .join(
                Prerequisite,
                Prerequisite.required_course_id
                == Course.course_id,
            )
            .where(
                Prerequisite.course_id
                == course_id
            )
            .order_by(
                Course.course_code
            )
        ).all()


    @staticmethod
    def get_attempts_for_course(
        db: Session,
        record_id: str,
        course_id: str,
    ):
        return db.scalars(
            select(CourseAttempt)
            .where(
                CourseAttempt.record_id
                == record_id,

                CourseAttempt.course_id
                == course_id,
            )
            .order_by(
                CourseAttempt.attempt_number
            )
        ).all()


    @staticmethod
    def get_term(
        db: Session,
        term_id: str,
    ):
        return db.get(
            AcademicTerm,
            term_id,
        )


    @staticmethod
    def get_active_offering(
        db: Session,
        course_id: str,
        term_id: str,
    ):
        return db.scalar(
            select(CourseOffering)
            .where(
                CourseOffering.course_id
                == course_id,

                CourseOffering.term_id
                == term_id,

                CourseOffering.status
                == "Active",
            )
        )


    @staticmethod
    def get_active_sections(
        db: Session,
        offering_id: str,
    ):
        return db.scalars(
            select(ClassSection)
            .where(
                ClassSection.offering_id
                == offering_id,

                ClassSection.status
                == "Active",
            )
            .order_by(
                ClassSection.section_code
            )
        ).all()


    @staticmethod
    def get_meetings(
        db: Session,
        section_id: str,
    ):
        return db.scalars(
            select(SectionMeeting)
            .where(
                SectionMeeting.section_id
                == section_id
            )
            .order_by(
                SectionMeeting.day_of_week,
                SectionMeeting.start_time,
            )
        ).all()
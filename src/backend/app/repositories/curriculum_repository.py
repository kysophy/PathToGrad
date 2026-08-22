from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.models import (
    AcademicProgram,
    Course,
    Curriculum,
    CurriculumCourse,
    Faculty,
    ProgramTrack,
)

GENERAL_SPEC_CODE = "GEN"


class CurriculumRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, curriculum_id: str) -> Curriculum | None:
        return self.session.get(Curriculum, curriculum_id)

    def get_by_program(self, program_id: str) -> Curriculum | None:
        return self.session.scalar(
            select(Curriculum)
            .where(Curriculum.program_id == program_id)
            .order_by(Curriculum.version)
        )

    def get_faculty(self, faculty_id: str) -> Faculty | None:
        return self.session.get(Faculty, faculty_id)

    def get_track(self, track_id: str) -> ProgramTrack | None:
        return self.session.get(ProgramTrack, track_id)

    def get_program(self, program_id: str) -> AcademicProgram | None:
        return self.session.scalar(
            select(AcademicProgram)
            .options(
                joinedload(AcademicProgram.faculty),
                joinedload(AcademicProgram.track),
            )
            .where(AcademicProgram.program_id == program_id)
        )

    def list_faculties(self) -> list[Faculty]:
        return list(
            self.session.scalars(select(Faculty).order_by(Faculty.name)).all()
        )

    def list_tracks(self) -> list[ProgramTrack]:
        return list(
            self.session.scalars(
                select(ProgramTrack).order_by(ProgramTrack.name)
            ).all()
        )

    def list_programs(
        self,
        faculty_id: str,
        track_id: str,
    ) -> list[AcademicProgram]:
        return list(
            self.session.scalars(
                select(AcademicProgram)
                .where(
                    AcademicProgram.faculty_id == faculty_id,
                    AcademicProgram.track_id == track_id,
                )
                .order_by(AcademicProgram.name)
            ).all()
        )

    def list_courses_for_student(
        self,
        curriculum_id: str,
        spec_code: str | None,
    ) -> list[tuple[CurriculumCourse, Course]]:
        spec_filter = CurriculumCourse.spec_code == GENERAL_SPEC_CODE
        if spec_code:
            spec_filter = or_(
                CurriculumCourse.spec_code == GENERAL_SPEC_CODE,
                CurriculumCourse.spec_code == spec_code,
            )

        return list(
            self.session.execute(
                select(CurriculumCourse, Course)
                .join(
                    Course,
                    Course.course_id == CurriculumCourse.course_id,
                )
                .where(
                    CurriculumCourse.curriculum_id == curriculum_id,
                    spec_filter,
                )
                .order_by(
                    CurriculumCourse.assigned_semester,
                    Course.course_code,
                )
            ).all()
        )

    def list_mandatory_courses(
        self,
        curriculum_id: str,
        spec_code: str | None,
    ) -> list[Course]:
        return [
            course
            for row, course in self.list_courses_for_student(
                curriculum_id,
                spec_code,
            )
            if row.requirement_type == "Core"
        ]

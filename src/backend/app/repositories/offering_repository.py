from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models import (
    AcademicTerm,
    ClassSection,
    CourseOffering,
    SectionMeeting,
)


class OfferingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_term(self, term_id: str) -> AcademicTerm | None:
        return self.session.get(AcademicTerm, term_id)

    def get_term_by_name(self, name: str) -> AcademicTerm | None:
        return self.session.scalar(
            select(AcademicTerm).where(AcademicTerm.name == name)
        )

    def list_terms(self) -> list[AcademicTerm]:
        return list(
            self.session.scalars(
                select(AcademicTerm).order_by(AcademicTerm.start_date)
            ).all()
        )

    def get_offering(
        self,
        course_id: str,
        term_id: str,
    ) -> CourseOffering | None:
        return self.session.scalar(
            select(CourseOffering).where(
                CourseOffering.course_id == course_id,
                CourseOffering.term_id == term_id,
            )
        )

    def get_active_offering(
        self,
        course_id: str,
        term_id: str,
    ) -> CourseOffering | None:
        return self.session.scalar(
            select(CourseOffering).where(
                CourseOffering.course_id == course_id,
                CourseOffering.term_id == term_id,
                CourseOffering.status == "Active",
            )
        )

    def list_active_sections(self, offering_id: str) -> list[ClassSection]:
        return list(
            self.session.scalars(
                select(ClassSection)
                .where(
                    ClassSection.offering_id == offering_id,
                    ClassSection.status == "Active",
                )
                .order_by(ClassSection.section_code)
            ).all()
        )

    def list_sections_with_meetings(
        self,
        offering_id: str,
    ) -> list[ClassSection]:
        return list(
            self.session.scalars(
                select(ClassSection)
                .options(selectinload(ClassSection.meetings))
                .where(
                    ClassSection.offering_id == offering_id,
                    ClassSection.status == "Active",
                )
                .order_by(ClassSection.section_code)
            ).all()
        )

    def get_meetings(self, section_id: str) -> list[SectionMeeting]:
        return list(
            self.session.scalars(
                select(SectionMeeting)
                .where(SectionMeeting.section_id == section_id)
                .order_by(
                    SectionMeeting.day_of_week,
                    SectionMeeting.start_time,
                )
            ).all()
        )

    def get_offering_with_sections(
        self,
        course_id: str,
        term_id: str,
    ) -> CourseOffering | None:
        return self.session.scalar(
            select(CourseOffering)
            .options(
                joinedload(CourseOffering.sections).selectinload(
                    ClassSection.meetings
                )
            )
            .where(
                CourseOffering.course_id == course_id,
                CourseOffering.term_id == term_id,
            )
        )

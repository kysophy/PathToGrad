from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import Course, Prerequisite


class CourseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, course_id: str) -> Course | None:
        return self.session.get(Course, course_id)

    def get_by_code(self, course_code: str) -> Course | None:
        return self.session.scalar(
            select(Course).where(Course.course_code == course_code)
        )

    def list_active(self) -> list[Course]:
        return list(
            self.session.scalars(
                select(Course)
                .where(Course.status == "Active")
                .order_by(Course.course_code)
            ).all()
        )

    def get_prerequisites(self, course_id: str) -> list[Course]:
        return list(
            self.session.scalars(
                select(Course)
                .join(
                    Prerequisite,
                    Prerequisite.required_course_id == Course.course_id,
                )
                .where(Prerequisite.course_id == course_id)
                .order_by(Course.course_code)
            ).all()
        )

    def get_graph(self, course_ids: list[str] | None = None) -> list[Prerequisite]:
        statement = select(Prerequisite)
        if course_ids:
            statement = statement.where(
                or_(
                    Prerequisite.course_id.in_(course_ids),
                    Prerequisite.required_course_id.in_(course_ids),
                )
            )
        return list(self.session.scalars(statement).all())

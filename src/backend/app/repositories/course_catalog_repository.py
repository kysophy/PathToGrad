from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course


class CourseCatalogRepository:

    @staticmethod
    def get_active_courses(
        db: Session,
    ):
        return db.scalars(
            select(Course)
            .where(
                Course.status == "Active"
            )
            .order_by(
                Course.course_code
            )
        ).all()
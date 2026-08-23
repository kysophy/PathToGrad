from pydantic import BaseModel

from app.schemas.enums import CoursePrimaryStatus


class CourseCatalogItemResponse(BaseModel):
    course_code: str
    course_name: str
    name_vi: str | None = None
    name_en: str | None = None
    credits: int
    assigned_semester: int | None = None
    is_mandatory: bool | None = None

    prerequisite_codes: list[str]

    prerequisite_eligible: bool | None

    offered: bool

    eligible: bool | None

    primary_status: CoursePrimaryStatus | None = None
    blocked: bool = False
    not_offered: bool = False

    warnings: list[str]
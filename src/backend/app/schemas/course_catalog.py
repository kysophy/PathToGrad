from pydantic import BaseModel


class CourseCatalogItemResponse(BaseModel):
    course_code: str
    course_name: str
    credits: int

    prerequisite_codes: list[str]

    prerequisite_eligible: bool | None

    offered: bool

    eligible: bool | None

    warnings: list[str]
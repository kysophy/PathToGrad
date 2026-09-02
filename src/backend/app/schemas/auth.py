from pydantic import BaseModel

from app.schemas.enums import UserRole


class LoginRequest(BaseModel):
    identifier: str
    password: str


class LoginResponse(BaseModel):
    role: UserRole
    name: str
    student_id: str | None = None

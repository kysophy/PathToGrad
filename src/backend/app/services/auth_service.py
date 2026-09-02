from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository
from app.schemas.auth import LoginRequest, LoginResponse


class AuthService:
    """
    Dev-scope auth: identifier is a student_id (the common case, looked up
    first) or falls back to an email lookup for non-student accounts.
    Passwords are compared as stored (seed data uses the placeholder
    'NOT_USED_DAY1'); replace with real hashing before this leaves
    dev/demo scope.
    """

    @staticmethod
    def login(
        db: Session,
        data: LoginRequest,
    ) -> LoginResponse:

        students = StudentRepository(db)

        profile = students.get_profile(data.identifier)

        if profile is not None:
            user = profile.user
        else:
            user = students.get_user_by_email(data.identifier)
            profile = user.student_profile if user else None

        if user is None or user.password != data.password:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials.",
            )

        if user.account_status != "Active":
            raise HTTPException(
                status_code=403,
                detail="This account is not active.",
            )

        return LoginResponse(
            role=user.role,
            name=user.full_name,
            student_id=profile.student_id if profile else None,
        )

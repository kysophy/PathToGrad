from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database import get_db
from app.repositories.student_repository import StudentRepository
from app.schemas.agent import (
    ChatRequest,
    ChatResponse,
    ExplainedPlanResponse,
    PlanGenerateRequest,
)
from app.services.agent_service import AgentService

router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"],
)


@router.post("/chat", response_model=ChatResponse)
def agent_chat(
    body: ChatRequest,
    db: Session = Depends(get_db),
):
    return AgentService(db).chat(
        body.message,
        student_id=body.student_id,
        term_id=body.term_id,
    )


@router.post("/plan", response_model=ExplainedPlanResponse)
def agent_plan(
    body: PlanGenerateRequest,
    db: Session = Depends(get_db),
):
    term_id = body.term_id or get_settings().DEFAULT_TERM_ID
    if StudentRepository(db).get_profile(body.student_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Student profile does not exist.",
        )
    return AgentService(db).generate_plan(
        body.student_id,
        term_id,
        target_credit_load=body.target_credit_load,
        include_retakes=body.include_retakes,
        note=body.note,
    )

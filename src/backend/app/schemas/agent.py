from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.schemas.enums import AgentRunStatus, GenerationMode


class AgentRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    run_id: str
    student_id: str
    generation_mode: GenerationMode
    provider: str | None
    status: AgentRunStatus
    latency_ms: int | None
    error: str | None
    created_at: datetime


class ToolCallRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tool_call_id: str
    run_id: str
    tool_name: str
    input_json: Any
    output_json: Any
    duration_ms: int | None
    success: bool
    created_at: datetime

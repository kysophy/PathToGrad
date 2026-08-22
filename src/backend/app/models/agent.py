from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.schemas.enums import AgentRunStatus, GenerationMode

_enum_values = lambda cls: [item.value for item in cls]


class AgentRun(Base):
    __tablename__ = "agent_run"

    run_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    student_id: Mapped[str] = mapped_column(
        ForeignKey("student_profile.student_id"),
        nullable=False,
    )

    generation_mode: Mapped[str] = mapped_column(
        Enum(*_enum_values(GenerationMode), name="agent_generation_mode"),
        nullable=False,
    )

    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)

    status: Mapped[str] = mapped_column(
        Enum(*_enum_values(AgentRunStatus), name="agent_run_status"),
        nullable=False,
        default=AgentRunStatus.STARTED.value,
    )

    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    student: Mapped["StudentProfile"] = relationship("StudentProfile")
    tool_calls: Mapped[list[ToolCall]] = relationship(
        back_populates="run",
    )


class ToolCall(Base):
    __tablename__ = "tool_call"

    tool_call_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    run_id: Mapped[str] = mapped_column(
        ForeignKey("agent_run.run_id"),
        nullable=False,
    )

    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)

    input_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    output_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)

    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    run: Mapped[AgentRun] = relationship(back_populates="tool_calls")

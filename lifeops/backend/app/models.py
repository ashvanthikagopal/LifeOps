from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    event_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    processed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    event_id: Mapped[int | None] = mapped_column(
        ForeignKey("events.id"),
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # ---------------------------------------
    # USER OBJECTIVE STATUS
    # ---------------------------------------

    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING"
    )

    # ---------------------------------------
    # RISK
    # ---------------------------------------

    risk_level: Mapped[str] = mapped_column(
        String(50),
        default="LOW"
    )

    # ---------------------------------------
    # WHAT LIFEOps IS ALLOWED TO DO
    # ---------------------------------------

    action_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    action_name: Mapped[str | None] = mapped_column(
    String(100),
    nullable=True,
    )

    # ---------------------------------------
    # USER APPROVAL
    # ---------------------------------------

    approval_status: Mapped[str] = mapped_column(
        String(50),
        default="NOT_REQUIRED"
    )

    # ---------------------------------------
    # WHAT LIFEOps DID
    # ---------------------------------------

    action_status: Mapped[str] = mapped_column(
        String(50),
        default="NOT_STARTED"
    )
    progress: Mapped[int] = mapped_column(
    Integer,
    default=0,
    )

    category: Mapped[str] = mapped_column(
    String(50),
    default="GENERAL",
    )

    priority: Mapped[str] = mapped_column(
    String(20),
    default="MEDIUM",
    )

    next_action: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True,
    )

    remaining_work: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
    )

    last_reasoning: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
    )

    # ---------------------------------------
    # HOW COMPLETION WAS VERIFIED
    # ---------------------------------------

    completion_source: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    action_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    executed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
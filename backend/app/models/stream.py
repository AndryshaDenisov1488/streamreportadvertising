from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class StreamEvent(Base):
    __tablename__ = "stream_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    duration_days: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    locked_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    content_url: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    days: Mapped[list["StreamDay"]] = relationship(
        "StreamDay", back_populates="stream_event", cascade="all, delete-orphan", order_by="StreamDay.day_index"
    )
    broadcast_sessions: Mapped[list["BroadcastSession"]] = relationship(
        "BroadcastSession", back_populates="stream_event", cascade="all, delete-orphan"
    )
    day_assignments: Mapped[list["StreamDayAssignment"]] = relationship(
        "StreamDayAssignment", back_populates="stream_event", cascade="all, delete-orphan"
    )
    event_logos: Mapped[list["StreamEventLogo"]] = relationship(
        "StreamEventLogo",
        back_populates="stream_event",
        cascade="all, delete-orphan",
        order_by="StreamEventLogo.sort_order",
    )


class StreamDayAssignment(Base):
    """Какой оператор ведёт конкретный день многодневного эфира (уникально по событию и дню)."""

    __tablename__ = "stream_day_assignments"
    __table_args__ = (
        UniqueConstraint("stream_event_id", "day_index", name="uq_stream_day_assignment_event_day"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    operator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    stream_event: Mapped["StreamEvent"] = relationship("StreamEvent", back_populates="day_assignments")


class StreamDay(Base):
    __tablename__ = "stream_days"
    __table_args__ = (UniqueConstraint("stream_event_id", "day_index", name="uq_stream_day_event_idx"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    stream_url: Mapped[str] = mapped_column(Text, default="", nullable=False)
    server_url: Mapped[str] = mapped_column(Text, default="", nullable=False)
    stream_key: Mapped[str] = mapped_column(Text, default="", nullable=False)

    stream_event: Mapped["StreamEvent"] = relationship("StreamEvent", back_populates="days")


class BroadcastSession(Base):
    __tablename__ = "broadcast_sessions"
    __table_args__ = (
        Index(
            "ix_broadcast_active_per_event_day",
            "stream_event_id",
            "day_index",
            unique=True,
            postgresql_where=text("ended_at IS NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    operator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_alert_last_sent_hour: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))

    stream_event: Mapped["StreamEvent"] = relationship("StreamEvent", back_populates="broadcast_sessions")
    mentions: Mapped[list["SponsorMention"]] = relationship(
        "SponsorMention", back_populates="broadcast_session", cascade="all, delete-orphan"
    )


class SponsorMention(Base):
    __tablename__ = "sponsor_mentions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    broadcast_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("broadcast_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    original_offset_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    adjusted_offset_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    broadcast_session: Mapped["BroadcastSession"] = relationship("BroadcastSession", back_populates="mentions")
    adjustments: Mapped[list["MentionAdjustment"]] = relationship(
        "MentionAdjustment", back_populates="mention", cascade="all, delete-orphan"
    )


class MentionAdjustment(Base):
    __tablename__ = "mention_adjustments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mention_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sponsor_mentions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    editor_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )
    previous_adjusted_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    new_adjusted_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    mention: Mapped["SponsorMention"] = relationship("SponsorMention", back_populates="adjustments")


class StreamEventTemplate(Base):
    """Шаблон события: название шаблона, заголовок эфира по умолчанию, дни (URL/ключи)."""

    __tablename__ = "stream_event_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    duration_days: Mapped[int] = mapped_column(SmallInteger(), nullable=False)
    days_json: Mapped[list] = mapped_column(JSONB, nullable=False)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

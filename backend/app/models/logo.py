import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Logo(Base):
    """Файл логотипа в медиатеке (переиспользуется между мероприятиями)."""

    __tablename__ = "logos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename_original: Mapped[str] = mapped_column(String(500), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    uploaded_by = relationship("User", foreign_keys=[uploaded_by_id])
    stream_links: Mapped[list["StreamEventLogo"]] = relationship(
        "StreamEventLogo", back_populates="logo", cascade="all, delete-orphan"
    )


class StreamEventLogo(Base):
    """Связь мероприятие ↔ логотип (многие-ко-многим с порядком)."""

    __tablename__ = "stream_event_logos"
    __table_args__ = (UniqueConstraint("stream_event_id", "logo_id", name="uq_stream_event_logo"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    logo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("logos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sort_order: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)

    stream_event = relationship("StreamEvent", back_populates="event_logos")
    logo = relationship("Logo", back_populates="stream_links")

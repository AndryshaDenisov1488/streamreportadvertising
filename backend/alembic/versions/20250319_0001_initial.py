"""initial schema

Revision ID: 0001
Revises:
Create Date: 2025-03-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    userrole = postgresql.ENUM("SUPERADMIN", "STREAM_MANAGER", "OPERATOR", name="userrole")
    userrole.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", userrole, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("jti", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("jti"),
    )
    op.create_index(op.f("ix_refresh_tokens_user_id"), "refresh_tokens", ["user_id"], unique=False)

    op.create_table(
        "stream_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("duration_days", sa.SmallInteger(), nullable=False),
        sa.Column("locked_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["locked_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stream_events_locked_by_user_id"), "stream_events", ["locked_by_user_id"], unique=False)

    op.create_table(
        "stream_days",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("stream_event_id", sa.Uuid(), nullable=False),
        sa.Column("day_index", sa.SmallInteger(), nullable=False),
        sa.Column("stream_url", sa.Text(), nullable=False),
        sa.Column("server_url", sa.Text(), nullable=False),
        sa.Column("stream_key", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["stream_event_id"], ["stream_events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stream_event_id", "day_index", name="uq_stream_day_event_idx"),
    )
    op.create_index(op.f("ix_stream_days_stream_event_id"), "stream_days", ["stream_event_id"], unique=False)

    op.create_table(
        "broadcast_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("stream_event_id", sa.Uuid(), nullable=False),
        sa.Column("day_index", sa.SmallInteger(), nullable=False),
        sa.Column("operator_id", sa.Uuid(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["operator_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["stream_event_id"], ["stream_events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_broadcast_sessions_stream_event_id"), "broadcast_sessions", ["stream_event_id"], unique=False)
    op.create_index(
        "ix_broadcast_active_per_event_day",
        "broadcast_sessions",
        ["stream_event_id", "day_index"],
        unique=True,
        postgresql_where=sa.text("ended_at IS NULL"),
    )

    op.create_table(
        "sponsor_mentions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("broadcast_session_id", sa.Uuid(), nullable=False),
        sa.Column("original_offset_sec", sa.Integer(), nullable=False),
        sa.Column("adjusted_offset_sec", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["broadcast_session_id"], ["broadcast_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_sponsor_mentions_broadcast_session_id"),
        "sponsor_mentions",
        ["broadcast_session_id"],
        unique=False,
    )

    op.create_table(
        "mention_adjustments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("mention_id", sa.Uuid(), nullable=False),
        sa.Column("editor_user_id", sa.Uuid(), nullable=False),
        sa.Column("previous_adjusted_sec", sa.Integer(), nullable=False),
        sa.Column("new_adjusted_sec", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["editor_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["mention_id"], ["sponsor_mentions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_mention_adjustments_mention_id"), "mention_adjustments", ["mention_id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("action_type", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=True),
        sa.Column("payload_before", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("payload_after", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_action_type"), "audit_logs", ["action_type"], unique=False)
    op.create_index(op.f("ix_audit_logs_created_at"), "audit_logs", ["created_at"], unique=False)
    op.create_index(op.f("ix_audit_logs_entity_id"), "audit_logs", ["entity_id"], unique=False)
    op.create_index(op.f("ix_audit_logs_user_id"), "audit_logs", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_user_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_created_at"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_action_type"), table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index(op.f("ix_mention_adjustments_mention_id"), table_name="mention_adjustments")
    op.drop_table("mention_adjustments")
    op.drop_index(op.f("ix_sponsor_mentions_broadcast_session_id"), table_name="sponsor_mentions")
    op.drop_table("sponsor_mentions")
    op.drop_index("ix_broadcast_active_per_event_day", table_name="broadcast_sessions")
    op.drop_index(op.f("ix_broadcast_sessions_stream_event_id"), table_name="broadcast_sessions")
    op.drop_table("broadcast_sessions")
    op.drop_index(op.f("ix_stream_days_stream_event_id"), table_name="stream_days")
    op.drop_table("stream_days")
    op.drop_index(op.f("ix_stream_events_locked_by_user_id"), table_name="stream_events")
    op.drop_table("stream_events")
    op.drop_index(op.f("ix_refresh_tokens_user_id"), table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    postgresql.ENUM("SUPERADMIN", "STREAM_MANAGER", "OPERATOR", name="userrole").drop(
        op.get_bind(),
        checkfirst=True,
    )

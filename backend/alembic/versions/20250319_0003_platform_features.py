"""notifications analytics invites checklist

Revision ID: 0003
Revises: 0002
Create Date: 2025-03-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("kind", sa.String(50), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "product_analytics_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("event_name", sa.String(100), nullable=False, index=True),
        sa.Column("meta", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "user_invites",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("token", sa.String(64), nullable=False, unique=True, index=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column(
            "role",
            sa.Enum("OPERATOR", "STREAM_MANAGER", "SUPERADMIN", name="userrole", create_type=False),
            nullable=False,
        ),
        sa.Column("created_by_user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "broadcast_checklists",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("stream_event_id", UUID(as_uuid=True), sa.ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mic_ok", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("scene_ok", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("sponsor_slots_ok", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("keys_tested_ok", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("stream_event_id", "user_id", name="uq_checklist_stream_user"),
    )
    op.create_index("ix_broadcast_checklists_stream_event_id", "broadcast_checklists", ["stream_event_id"])


def downgrade() -> None:
    op.drop_index("ix_broadcast_checklists_stream_event_id", table_name="broadcast_checklists")
    op.drop_table("broadcast_checklists")
    op.drop_table("user_invites")
    op.drop_table("product_analytics_events")
    op.drop_table("notifications")

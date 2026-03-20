"""logos, stream_event_logos, content_url

Revision ID: 0010
Revises: 0009
Create Date: 2025-03-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0010"
down_revision: Union[str, None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "logos",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("filename_original", sa.String(length=500), nullable=False),
        sa.Column("stored_path", sa.String(length=1000), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("uploaded_by_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["uploaded_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_logos_uploaded_by_id"), "logos", ["uploaded_by_id"], unique=False)

    op.create_table(
        "stream_event_logos",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("stream_event_id", sa.Uuid(), nullable=False),
        sa.Column("logo_id", sa.Uuid(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["stream_event_id"], ["stream_events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["logo_id"], ["logos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("stream_event_id", "logo_id", name="uq_stream_event_logo"),
    )
    op.create_index(
        op.f("ix_stream_event_logos_stream_event_id"), "stream_event_logos", ["stream_event_id"], unique=False
    )
    op.create_index(op.f("ix_stream_event_logos_logo_id"), "stream_event_logos", ["logo_id"], unique=False)

    op.add_column("stream_events", sa.Column("content_url", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("stream_events", "content_url")
    op.drop_index(op.f("ix_stream_event_logos_logo_id"), table_name="stream_event_logos")
    op.drop_index(op.f("ix_stream_event_logos_stream_event_id"), table_name="stream_event_logos")
    op.drop_table("stream_event_logos")
    op.drop_index(op.f("ix_logos_uploaded_by_id"), table_name="logos")
    op.drop_table("logos")

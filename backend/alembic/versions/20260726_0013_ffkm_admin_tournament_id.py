"""ffkm_admin_tournament_id on stream_events

Revision ID: 0013
Revises: 0012
Create Date: 2026-07-26

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0013"
down_revision: Union[str, None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "stream_events",
        sa.Column("ffkm_admin_tournament_id", sa.Integer(), nullable=True),
    )
    op.create_index(
        "ix_stream_events_ffkm_admin_tournament_id",
        "stream_events",
        ["ffkm_admin_tournament_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_stream_events_ffkm_admin_tournament_id", table_name="stream_events")
    op.drop_column("stream_events", "ffkm_admin_tournament_id")

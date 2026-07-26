"""ffkm_admin_rank on stream_events

Revision ID: 0014
Revises: 0013
Create Date: 2026-07-26

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0014"
down_revision: Union[str, None] = "0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "stream_events",
        sa.Column("ffkm_admin_rank", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_stream_events_ffkm_admin_rank", "stream_events", ["ffkm_admin_rank"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_stream_events_ffkm_admin_rank", table_name="stream_events")
    op.drop_column("stream_events", "ffkm_admin_rank")

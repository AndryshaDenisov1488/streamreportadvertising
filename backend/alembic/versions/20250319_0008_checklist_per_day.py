"""checklist per day + 6 items

Revision ID: 0008
Revises: 0007
Create Date: 2025-03-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "broadcast_checklists",
        sa.Column("day_index", sa.Integer(), nullable=False, server_default="1"),
    )
    op.drop_constraint("uq_checklist_stream_user", "broadcast_checklists", type_="unique")
    op.create_unique_constraint(
        "uq_checklist_stream_user_day",
        "broadcast_checklists",
        ["stream_event_id", "user_id", "day_index"],
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("picture_exposure_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("judges_stream_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("splitter_socket_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("key_stream_started_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("kick_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("mentions_four_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.drop_column("broadcast_checklists", "mic_ok")
    op.drop_column("broadcast_checklists", "scene_ok")
    op.drop_column("broadcast_checklists", "sponsor_slots_ok")
    op.drop_column("broadcast_checklists", "keys_tested_ok")
    op.alter_column("broadcast_checklists", "day_index", server_default=None)


def downgrade() -> None:
    op.add_column(
        "broadcast_checklists",
        sa.Column("mic_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("scene_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("sponsor_slots_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "broadcast_checklists",
        sa.Column("keys_tested_ok", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.drop_column("broadcast_checklists", "picture_exposure_ok")
    op.drop_column("broadcast_checklists", "judges_stream_ok")
    op.drop_column("broadcast_checklists", "splitter_socket_ok")
    op.drop_column("broadcast_checklists", "key_stream_started_ok")
    op.drop_column("broadcast_checklists", "kick_ok")
    op.drop_column("broadcast_checklists", "mentions_four_ok")
    op.drop_constraint("uq_checklist_stream_user_day", "broadcast_checklists", type_="unique")
    op.create_unique_constraint(
        "uq_checklist_stream_user",
        "broadcast_checklists",
        ["stream_event_id", "user_id"],
    )
    op.drop_column("broadcast_checklists", "day_index")

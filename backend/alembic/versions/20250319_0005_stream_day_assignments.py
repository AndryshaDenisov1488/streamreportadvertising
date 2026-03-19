"""stream_day_assignments: операторы по дням турнира"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stream_day_assignments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "stream_event_id",
            UUID(as_uuid=True),
            sa.ForeignKey("stream_events.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("day_index", sa.SmallInteger(), nullable=False),
        sa.Column(
            "operator_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.UniqueConstraint("stream_event_id", "day_index", name="uq_stream_day_assignment_event_day"),
    )
    op.create_index("ix_stream_day_assignments_event", "stream_day_assignments", ["stream_event_id"])

    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            INSERT INTO stream_day_assignments (id, stream_event_id, day_index, operator_id)
            SELECT gen_random_uuid(), e.id, d.day_idx, e.locked_by_user_id
            FROM stream_events e
            CROSS JOIN LATERAL generate_series(1, e.duration_days::integer) AS d(day_idx)
            WHERE e.locked_by_user_id IS NOT NULL
            """
        )
    )


def downgrade() -> None:
    op.drop_index("ix_stream_day_assignments_event", table_name="stream_day_assignments")
    op.drop_table("stream_day_assignments")

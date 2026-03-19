"""onboarding_completed — интерактивное знакомство при первом входе

Revision ID: 0007
Revises: 0006
Create Date: 2025-03-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "onboarding_completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    # Уже существовавшие учётки не гоняем через тур повторно
    op.execute(sa.text("UPDATE users SET onboarding_completed = true"))
    op.alter_column("users", "onboarding_completed", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "onboarding_completed")

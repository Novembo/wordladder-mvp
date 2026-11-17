"""Allow full UUID hex identifiers for matches."""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9b2f4a6c1d30"
down_revision: Union[str, Sequence[str], None] = "36a7f11c9e02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("match_records") as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=8),
            type_=sa.String(length=32),
            existing_nullable=False,
        )
    with op.batch_alter_table("move_records") as batch_op:
        batch_op.alter_column(
            "match_id",
            existing_type=sa.String(length=8),
            type_=sa.String(length=32),
            existing_nullable=False,
        )


def downgrade() -> None:
    # Shrinking UUID values to eight characters risks collisions and data loss.
    raise RuntimeError("This migration is forward-only: match UUIDs cannot be safely shortened.")

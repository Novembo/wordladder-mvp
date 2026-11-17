"""expand match identifiers to full uuid

Revision ID: 43ac111f0874
Revises: 9b2f4a6c1d30
Create Date: 2026-11-17 08:38:13.406394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43ac111f0874'
down_revision: Union[str, Sequence[str], None] = '9b2f4a6c1d30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("match_records") as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.String(length=32),
            type_=sa.String(length=36),
            existing_nullable=False,
        )
    with op.batch_alter_table("move_records") as batch_op:
        batch_op.alter_column(
            "match_id",
            existing_type=sa.String(length=32),
            type_=sa.String(length=36),
            existing_nullable=False,
        )


def downgrade() -> None:
    # Shrinking UUID values risks collisions and data loss.
    raise RuntimeError("This migration is forward-only.")

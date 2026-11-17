"""expand match identifiers to full uuid

Revision ID: cf206e817fc7
Revises: 43ac111f0874
Create Date: 2026-11-17 08:38:29.813112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf206e817fc7'
down_revision: Union[str, Sequence[str], None] = '43ac111f0874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

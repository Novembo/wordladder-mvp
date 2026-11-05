"""Add user accounts, browser sessions, and match ownership.

Revision ID: 36a7f11c9e02
Revises: 280b92e91b41
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "36a7f11c9e02"
down_revision: Union[str, Sequence[str], None] = "280b92e91b41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("username_normalized", sa.String(length=20), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username_normalized"),
    )
    op.create_table(
        "user_sessions",
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("csrf_token", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("token_hash"),
    )
    op.create_index("ix_user_sessions_user_id", "user_sessions", ["user_id"])
    op.create_index("ix_user_sessions_expires_at", "user_sessions", ["expires_at"])
    op.create_table(
        "login_attempts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username_normalized", sa.String(length=20), nullable=False),
        sa.Column("ip_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_login_attempts_username_normalized",
        "login_attempts",
        ["username_normalized"],
    )
    op.create_index("ix_login_attempts_ip_hash", "login_attempts", ["ip_hash"])
    op.create_index("ix_login_attempts_created_at", "login_attempts", ["created_at"])
    with op.batch_alter_table("match_records") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_match_records_user_id_users",
            "users",
            ["user_id"],
            ["id"],
            ondelete="SET NULL",
        )
    op.create_index("ix_match_records_user_id", "match_records", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_match_records_user_id", table_name="match_records")
    with op.batch_alter_table("match_records") as batch_op:
        batch_op.drop_constraint("fk_match_records_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")
    op.drop_index("ix_login_attempts_created_at", table_name="login_attempts")
    op.drop_index("ix_login_attempts_ip_hash", table_name="login_attempts")
    op.drop_index(
        "ix_login_attempts_username_normalized", table_name="login_attempts"
    )
    op.drop_table("login_attempts")
    op.drop_index("ix_user_sessions_expires_at", table_name="user_sessions")
    op.drop_index("ix_user_sessions_user_id", table_name="user_sessions")
    op.drop_table("user_sessions")
    op.drop_table("users")

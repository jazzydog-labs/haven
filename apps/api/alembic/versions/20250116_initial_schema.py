"""Initial schema creation

Revision ID: 001_initial
Revises:
Create Date: 2025-01-16 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create initial database schema."""
    # Create records table
    op.create_table(
        "records",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create index on created_at for sorting
    op.create_index(op.f("ix_records_created_at"), "records", ["created_at"], unique=False)

    # Create index on updated_at for filtering
    op.create_index(op.f("ix_records_updated_at"), "records", ["updated_at"], unique=False)


def downgrade() -> None:
    """Drop initial database schema."""
    op.drop_index(op.f("ix_records_updated_at"), table_name="records")
    op.drop_index(op.f("ix_records_created_at"), table_name="records")
    op.drop_table("records")

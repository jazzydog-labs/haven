"""add_review_comments_table

Revision ID: b1babe0f8b3b
Revises: 20250716_2040
Create Date: 2025-07-17 00:51:31.784224+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1babe0f8b3b"
down_revision: str | None = "20250716_2040"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade database schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "review_comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("commit_id", sa.Integer(), nullable=False),
        sa.Column("reviewer_id", sa.Integer(), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=True),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["commit_id"],
            ["commits.id"],
        ),
        sa.ForeignKeyConstraint(
            ["reviewer_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_review_comments_commit_id"), "review_comments", ["commit_id"], unique=False
    )
    op.create_index(
        op.f("ix_review_comments_file_path"), "review_comments", ["file_path"], unique=False
    )
    op.create_index(op.f("ix_review_comments_id"), "review_comments", ["id"], unique=False)
    op.create_index(
        op.f("ix_review_comments_line_number"), "review_comments", ["line_number"], unique=False
    )
    op.create_index(
        op.f("ix_review_comments_reviewer_id"), "review_comments", ["reviewer_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_review_comments_reviewer_id"), table_name="review_comments")
    op.drop_index(op.f("ix_review_comments_line_number"), table_name="review_comments")
    op.drop_index(op.f("ix_review_comments_id"), table_name="review_comments")
    op.drop_index(op.f("ix_review_comments_file_path"), table_name="review_comments")
    op.drop_index(op.f("ix_review_comments_commit_id"), table_name="review_comments")
    op.drop_table("review_comments")
    # ### end Alembic commands ###

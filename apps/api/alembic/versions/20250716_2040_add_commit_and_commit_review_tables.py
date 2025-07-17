"""add_commit_and_commit_review_tables

Revision ID: 20250716_2040
Revises: 20250716_2014
Create Date: 2025-07-16 20:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250716_2040'
down_revision = '25c03bf94ce3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create commits table
    op.create_table(
        'commits',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('repository_id', sa.Integer(), sa.ForeignKey('repositories.id'), nullable=False, index=True),
        sa.Column('commit_hash', sa.String(64), nullable=False, index=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('author_name', sa.String(255), nullable=False),
        sa.Column('author_email', sa.String(255), nullable=False),
        sa.Column('committer_name', sa.String(255), nullable=False),
        sa.Column('committer_email', sa.String(255), nullable=False),
        sa.Column('committed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('files_changed', sa.Integer(), nullable=False, default=0),
        sa.Column('insertions', sa.Integer(), nullable=False, default=0),
        sa.Column('deletions', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint('repository_id', 'commit_hash', name='_repository_commit_hash_uc'),
    )
    
    # Create commit_reviews table
    op.create_table(
        'commit_reviews',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('commit_id', sa.Integer(), sa.ForeignKey('commits.id'), nullable=False, index=True),
        sa.Column('reviewer_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('status', sa.String(50), nullable=False, default='pending_review', index=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('commit_reviews')
    op.drop_table('commits')
"""add_repository_hash_and_remote_url

Revision ID: 0776b841d098
Revises: 55fa54dcd01a
Create Date: 2025-07-17 14:41:37.150580+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0776b841d098'
down_revision: Union[str, None] = '55fa54dcd01a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade database schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('repositories', sa.Column('repository_hash', sa.String(length=64), nullable=True))
    op.add_column('repositories', sa.Column('remote_url', sa.Text(), nullable=True))
    op.create_index(op.f('ix_repositories_repository_hash'), 'repositories', ['repository_hash'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_repositories_repository_hash'), table_name='repositories')
    op.drop_column('repositories', 'remote_url')
    op.drop_column('repositories', 'repository_hash')
    # ### end Alembic commands ###
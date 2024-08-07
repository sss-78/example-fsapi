"""create posts table

Revision ID: 7628af397f43
Revises: 
Create Date: 2024-08-06 14:17:09.425966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7628af397f43'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')

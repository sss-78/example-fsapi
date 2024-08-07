"""add content column"


Revision ID: 1d65c3617d97
Revises: 7628af397f43
Create Date: 2024-08-06 14:37:46.261432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d65c3617d97'
down_revision: Union[str, None] = '7628af397f43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')

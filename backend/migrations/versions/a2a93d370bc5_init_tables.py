"""Init tables

Revision ID: a2a93d370bc5
Revises: 
Create Date: 2023-10-27 21:38:47.799759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2a93d370bc5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('postcards',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('is_liked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postcards')
    # ### end Alembic commands ###

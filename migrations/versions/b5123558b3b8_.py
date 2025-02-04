"""empty message

Revision ID: b5123558b3b8
Revises: e30488be30e9
Create Date: 2024-04-20 22:56:04.455541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5123558b3b8'
down_revision: Union[str, None] = 'e30488be30e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modify_date', sa.DateTime(), nullable=True))

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('modify_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('modify_date')

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_column('modify_date')

    # ### end Alembic commands ###

"""empty message

Revision ID: 95198662e50a
Revises: 7ec352b2dfec
Create Date: 2025-01-12 15:14:44.942417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95198662e50a'
down_revision = '7ec352b2dfec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')

    # ### end Alembic commands ###

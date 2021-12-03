"""update db

Revision ID: d674f663efc2
Revises: 0a2a5bb379a4
Create Date: 2021-10-01 17:21:04.520678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd674f663efc2'
down_revision = '0a2a5bb379a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff', sa.Column('have_account', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staff', 'have_account')
    # ### end Alembic commands ###

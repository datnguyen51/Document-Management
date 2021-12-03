"""update db

Revision ID: 95ad4f003ca7
Revises: c5b25c4e4cbe
Create Date: 2021-10-25 15:06:42.881053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95ad4f003ca7'
down_revision = 'c5b25c4e4cbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('document_expire', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 'document_expire')
    # ### end Alembic commands ###

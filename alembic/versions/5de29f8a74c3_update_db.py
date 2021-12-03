"""update db

Revision ID: 5de29f8a74c3
Revises: c376c96337f0
Create Date: 2021-11-01 15:30:46.603334

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5de29f8a74c3'
down_revision = 'c376c96337f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('release_code', sa.String(length=250), nullable=True))
    op.add_column('document', sa.Column('comment', sa.String(length=2500), nullable=True))
    op.drop_constraint('document_staff_id_fkey', 'document', type_='foreignkey')
    op.drop_column('document', 'staff_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('staff_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('document_staff_id_fkey', 'document', 'staff', ['staff_id'], ['id'])
    op.drop_column('document', 'comment')
    op.drop_column('document', 'release_code')
    # ### end Alembic commands ###
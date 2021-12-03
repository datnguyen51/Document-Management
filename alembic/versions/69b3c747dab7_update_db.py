"""update db

Revision ID: 69b3c747dab7
Revises: d674f663efc2
Create Date: 2021-10-11 08:30:07.824326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '69b3c747dab7'
down_revision = 'd674f663efc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('document_parent_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('document', sa.Column('document_parent_name', sa.String(), nullable=True))
    op.create_foreign_key(None, 'document', 'document', ['document_parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'document', type_='foreignkey')
    op.drop_column('document', 'document_parent_name')
    op.drop_column('document', 'document_parent_id')
    # ### end Alembic commands ###
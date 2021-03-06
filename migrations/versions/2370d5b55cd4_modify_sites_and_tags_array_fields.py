"""modify sites and tags array fields

Revision ID: 2370d5b55cd4
Revises: 844fbeba4059
Create Date: 2020-12-07 21:12:51.918148

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2370d5b55cd4'
down_revision = '844fbeba4059'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('sites', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.drop_column('tags', 'site')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('site', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.drop_column('tags', 'sites')
    # ### end Alembic commands ###

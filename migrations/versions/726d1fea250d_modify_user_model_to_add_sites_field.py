"""modify user model to add sites field

Revision ID: 726d1fea250d
Revises: 2370d5b55cd4
Create Date: 2020-12-09 11:41:38.143715

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '726d1fea250d'
down_revision = '2370d5b55cd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sites', postgresql.ARRAY(sa.Integer(), dimensions=1), server_default='{}', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'sites')
    # ### end Alembic commands ###

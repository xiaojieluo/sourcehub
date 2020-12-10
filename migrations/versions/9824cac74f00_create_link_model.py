"""create link model

Revision ID: 9824cac74f00
Revises: 726d1fea250d
Create Date: 2020-12-09 12:25:27.266035

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9824cac74f00'
down_revision = '726d1fea250d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('links',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('tags', postgresql.ARRAY(sa.Integer(), dimensions=1), server_default='{}', nullable=True),
    sa.Column('pic', sa.String(length=255), nullable=True),
    sa.Column('vote', sa.Integer(), nullable=True),
    sa.Column('star', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('followers', postgresql.ARRAY(sa.Integer(), dimensions=1), server_default='{}', nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('links')
    # ### end Alembic commands ###

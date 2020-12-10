"""init

Revision ID: 1dab333572d9
Revises: 
Create Date: 2020-12-03 12:28:34.115296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dab333572d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appid', sa.String(length=255), nullable=True),
    sa.Column('appkey', sa.String(length=255), nullable=True),
    sa.Column('appmaster', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('appid')
    )
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('tags', sa.ARRAY(sa.Integer(), dimensions=1), nullable=True),
    sa.Column('pic', sa.String(length=255), nullable=True),
    sa.Column('vote', sa.Integer(), nullable=True),
    sa.Column('star', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('followers', sa.ARRAY(sa.Integer(), dimensions=1), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('sites', sa.ARRAY(sa.Integer(), dimensions=1), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('sessionToken', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('last_login', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('tags')
    op.drop_table('sites')
    op.drop_table('app')
    # ### end Alembic commands ###
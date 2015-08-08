"""empty message

Revision ID: 5fc494c4c8
Revises: 33f61f82edb
Create Date: 2015-08-08 11:49:38.208973

"""

# revision identifiers, used by Alembic.
revision = '5fc494c4c8'
down_revision = '33f61f82edb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###
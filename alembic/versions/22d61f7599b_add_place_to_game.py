"""Add place to game

Revision ID: 22d61f7599b
Revises: 40903a23149
Create Date: 2015-02-09 18:07:27.752483

"""

# revision identifiers, used by Alembic.
revision = '22d61f7599b'
down_revision = '40903a23149'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, ForeignKey


def upgrade():
    op.add_column(
        'games', Column('place_id', Integer, ForeignKey('places.id')))


def downgrade():
    op.drop_column('games', 'place_id')

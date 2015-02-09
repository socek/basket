"""Create place

Revision ID: 40903a23149
Revises: 3b93d1788cc
Create Date: 2015-02-09 18:06:57.052102

"""

# revision identifiers, used by Alembic.
revision = '40903a23149'
down_revision = '3b93d1788cc'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, String


def upgrade():
    op.create_table(
        'places',
        Column('id', Integer, primary_key=True),
        Column('name', String(), nullable=False),
    )


def downgrade():
    op.drop_table('places')

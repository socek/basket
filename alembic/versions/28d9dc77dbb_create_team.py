"""create_team

Revision ID: 28d9dc77dbb
Revises:
Create Date: 2015-02-06 10:53:22.008480

"""

# revision identifiers, used by Alembic.
revision = '28d9dc77dbb'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, String


def upgrade():
    op.create_table(
        'teams',
        Column('id', Integer, primary_key=True),
        Column('name', String(), nullable=False),
        Column('hometown', String(), nullable=False),
    )


def downgrade():
    op.drop_table('teams')

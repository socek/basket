"""Create group

Revision ID: 48a5b76dbc1
Revises: 28d9dc77dbb
Create Date: 2015-02-06 10:55:22.664198

"""

# revision identifiers, used by Alembic.
revision = '48a5b76dbc1'
down_revision = '28d9dc77dbb'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, String


def upgrade():
    op.create_table(
        'groups',
        Column('id', Integer, primary_key=True),
        Column('name', String(), nullable=False),
        Column('info', String()),
    )


def downgrade():
    op.drop_table('groups')

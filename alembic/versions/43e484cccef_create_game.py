"""Create Game

Revision ID: 43e484cccef
Revises: 1c8782e6b83
Create Date: 2015-02-06 11:10:54.748128

"""

# revision identifiers, used by Alembic.
revision = '43e484cccef'
down_revision = '1c8782e6b83'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String


def upgrade():
    op.create_table(
        'games',
        Column('id', Integer, primary_key=True),
        Column('index', Integer),
        Column('date', DateTime),
        Column(
            'left_team_id', Integer, ForeignKey('teams.id'), nullable=False),
        Column(
            'right_team_id', Integer, ForeignKey('teams.id'), nullable=False),
        Column('_status', String, default='not started')
    )


def downgrade():
    op.drop_table('games')

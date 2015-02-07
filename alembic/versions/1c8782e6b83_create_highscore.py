"""Create highscore

Revision ID: 1c8782e6b83
Revises: 48a5b76dbc1
Create Date: 2015-02-06 11:02:04.478660

"""

# revision identifiers, used by Alembic.
revision = '1c8782e6b83'
down_revision = '48a5b76dbc1'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, ForeignKey


def upgrade():
    op.create_table(
        'highscores',
        Column('id', Integer, primary_key=True),
        Column('index', Integer, nullable=False),
        Column('team_id', Integer, ForeignKey('teams.id'), nullable=False),
    )


def downgrade():
    op.drop_table('highscores')

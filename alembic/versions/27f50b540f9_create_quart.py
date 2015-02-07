"""Create Quart

Revision ID: 27f50b540f9
Revises: 43e484cccef
Create Date: 2015-02-06 11:17:41.778906

"""

# revision identifiers, used by Alembic.
revision = '27f50b540f9'
down_revision = '43e484cccef'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, ForeignKey


def upgrade():
    op.create_table(
        'quarts',
        Column('id', Integer, primary_key=True),
        Column('index', Integer),
        Column('left_score', Integer),
        Column('right_score', Integer),
        Column('game_id', Integer, ForeignKey('games.id'), nullable=False),
    )


def downgrade():
    op.drop_table('quarts')

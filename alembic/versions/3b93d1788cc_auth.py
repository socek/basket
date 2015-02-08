"""auth

Revision ID: 3b93d1788cc
Revises: 27f50b540f9
Create Date: 2015-02-08 12:29:06.918834

"""

# revision identifiers, used by Alembic.
revision = '3b93d1788cc'
down_revision = '27f50b540f9'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey


def upgrade():
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True),
        Column('name', String()),
        Column('email', String, unique=True),
        Column('password', String(128))
    )

    op.create_table(
        'permissions',
        Column('id', Integer, primary_key=True),
        Column('name', String()),
        Column('group', String()),
        UniqueConstraint('name', 'group'),
    )

    op.create_table(
        'users_2_permissions',
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('permission_id', Integer, ForeignKey('permissions.id'))
    )


def downgrade():
    op.drop_table('users_2_permissions')
    op.drop_table('permissions')
    op.drop_table('users')

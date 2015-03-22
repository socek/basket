from haplugin.sql.driver import SqlDriver

from .models import Group


class GroupDriver(SqlDriver):
    name = 'Group'
    model = Group

    def get_by_name(self, name):
        return self.db.query(Group).filter(Group.name == name).one()

from haplugin.sql.driver import SqlDriver

from .models import Team


class TeamDriver(SqlDriver):
    name = 'Team'
    model = Team

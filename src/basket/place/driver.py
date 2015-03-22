from haplugin.sql.driver import SqlDriver

from .models import Place


class PlaceDriver(SqlDriver):
    name = 'Place'
    model = Place

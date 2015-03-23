from haplugin.sql.driver import SqlDriver

from .models import Game


class GameDriver(SqlDriver):
    name = 'Game'
    model = Game

    def get_all(self):
        return super().get_all().order_by(Game.index)

    def get_all_order_by_date(self):
        return super().get_all().order_by(Game.date)

    def get_running(self):
        return self.get_all().filter(Game._status == 'running')

    def create(self, **kwargs):
        obj = super().create(**kwargs)
        self._add_quarts(obj)
        self.db.add(obj)
        return obj

    def _add_quarts(self, obj):
        for quart in obj.create_dependencies():
            self.db.add(quart)

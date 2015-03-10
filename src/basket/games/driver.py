from haplugin.driver import DriverGroup

from .models import Game


class SqlDriver(DriverGroup):

    def get_by_id(self, id):
        return self.get_all().filter_by(id=id).one()

    def get_all(self):
        return self.query(self.model)

    def create(self, **kwargs):
        obj = self.model()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        return obj


class GameDriver(SqlDriver):
    name = 'Game'
    model = Game

    def get_all(self):
        return super().get_all().order_by(Game.index)

    def get_running(self):
        return self.get_all().filter(Game._status == 'running')

    def create(self, **kwargs):
        obj = super().create(**kwargs)
        for quart in obj.create_dependencies():
            self.db.add(quart)
        self.db.add(obj)
        return obj

from haplugin.sql import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class StatusBased(object):

    _avalible_statuses = [
        'not started',
        'running',
        'ended'
    ]

    def _get_status(self):
        return self._status

    def _set_status(self, value):
        if value not in self._avalible_statuses:
            raise ValueError(
                '{0} is not in {1}'.format(value, self._avalible_statuses))
        self._status = value

    status = property(_get_status, _set_status)


class Game(Base, StatusBased):
    __tablename__ = 'games'
    _quarts = 4

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    date = Column(DateTime)

    left_team_id = Column(
        Integer, ForeignKey('teams.id'), nullable=False)
    left_team = relationship(
        "Team", primaryjoin='Game.left_team_id==Team.id')
    right_team_id = Column(
        Integer, ForeignKey('teams.id'), nullable=False)
    right_team = relationship(
        "Team", primaryjoin='Game.right_team_id==Team.id')
    quarts = relationship("Quart", order_by="Quart.index")

    _status = Column(String, default='not started')

    def create_dependencies(self):
        needed_quarts = list(range(self._quarts))
        for quart in self.quarts:
            needed_quarts.remove(quart.index)

        for index in needed_quarts:
            quart = Quart()
            quart.index = index
            quart.game = self
            yield quart

    def add_to_db_session(self, db):
        for quart in self.create_dependencies():
            db.add(quart)
        db.add(self)

    def delete(self, db):
        for quart in self.quarts:
            db.delete(quart)
        db.delete(self)


class Quart(Base):
    __tablename__ = 'quarts'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    left_score = Column(Integer)
    right_score = Column(Integer)

    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship("Game")

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

    _status = Column(String, default='not started')


class Quart(Base):
    __tablename__ = 'quarts'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    left_score = Column(Integer)
    right_score = Column(Integer)

    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship("Game", backref='quarts')

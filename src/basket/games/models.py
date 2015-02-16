from haplugin.sql import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from basket.teams.models import Team
from basket.groups.models import Group
from basket.place.models import Place


class StatusBased(object):

    _avalible_statuses = [
        'not started',
        'running',
        'ended'
    ]

    labels = {
        'not started': 'Nie rozpoczęto',
        'running': 'Trwa',
        'ended': 'Zakończony',
    }

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

    left_team_id = Column(Integer, ForeignKey('teams.id'))
    left_team = relationship(Team, primaryjoin=left_team_id == Team.id)

    right_team_id = Column(Integer, ForeignKey('teams.id'))
    right_team = relationship(Team, primaryjoin=right_team_id == Team.id)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship(Group, backref="games")

    place_id = Column(Integer, ForeignKey('places.id'))
    place = relationship(Place)

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

    def get_report(self):
        data = {
            'index': self.index,
            'date': self.date,
            'status': self.status,
            'group_name': self.group.name,
            'place': self.place.name,
        }
        if self.left_team:
            data['left'] = {
                'team': self.left_team.name,
                'quarts': [
                    quart.left_score for quart in self.quarts
                ]
            }
        else:
            data['left'] = {
                'team': '',
                'quarts': [None, None, None, None],
            }
        if self.right_team:
            data['right'] = {
                'team': self.right_team.name,
                'quarts': [
                    quart.right_score for quart in self.quarts
                ]
            }
        else:
            data['right'] = {
                'team': '',
                'quarts': [None, None, None, None],
            }
        data['left']['sum'] = sum(filter(None, data['left']['quarts']))
        data['right']['sum'] = sum(filter(None, data['right']['quarts']))
        return data


class Quart(Base):
    __tablename__ = 'quarts'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    left_score = Column(Integer)
    right_score = Column(Integer)

    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship("Game")

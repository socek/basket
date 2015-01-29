from haplugin.sql import Base
from sqlalchemy import Column, Integer, String, DateTime


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
    match_number = Column(Integer)
    date = Column(DateTime)

    _status = Column(String, default='not started')

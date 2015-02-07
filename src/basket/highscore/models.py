from haplugin.sql import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class HighScore(Base):
    __tablename__ = 'highscores'

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Team")

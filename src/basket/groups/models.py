from haplugin.sql import Base
from sqlalchemy import Column, Integer, String


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    info = Column(String)

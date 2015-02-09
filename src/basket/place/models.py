from haplugin.sql import Base
from sqlalchemy import Column, Integer, String


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String)

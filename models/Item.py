from sqlalchemy import Column, String, Text, ForeignKey, Integer

from models import Base


class Item(Base):

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'))
    name = Column(String(64))
    description = Column(Text)

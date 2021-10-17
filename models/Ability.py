from sqlalchemy import Column, String, Text, ForeignKey, Integer

from models import Base


class Ability(Base):

    __tablename__ = 'ability'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'))
    name = Column(String(64))
    description = Column(Text)

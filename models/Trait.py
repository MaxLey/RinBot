from sqlalchemy import Column, String, Text, ForeignKey, Integer

from models import Base

class Trait(Base):

    __tablename__ = 'trait'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'))
    name = Column(String(64))
    description = Column(Text)

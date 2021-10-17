from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

import DBManager
from models import Character, Base


class Mun(Base):

    __tablename__ = 'mun'
    id = Column(Integer, primary_key=True)
    characters = relationship("Character")
    active_character = Column(String)

    def generate_character_id(self, character_name): #TODO fix better ids, see note in character
        return self.id + '.' + character_name



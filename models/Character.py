from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

import DBManager
from models import Base


class Character(Base):

#TODO make DB access class?
#TODO add relationships
#TODO add more expansive lore

    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    mun = Column(Integer, ForeignKey('mun.id'))
    name = Column(String(64))
    pronoun_obj = Column(String(64))
    pronoun_subj = Column(String(64))
    #stats = relationship("StatObject", cascade="all, delete")
    sprite_url = Column(String(1024))
    thumbnail_url = Column(String(1024))
    str_base = Column(Integer)
    def_base = Column(Integer)
    mag_base = Column(Integer)
    agi_base = Column(Integer)
    abilities = relationship("Ability", cascade="all, delete")
    items = relationship("Item", cascade="all, delete")

    age = Column(Integer)
    height = Column(Integer)
    gender = Column(String(64))
    tribe = Column(String(255))
    occupation = Column(String(255))
    description = Column(String(2000))
    lore = Column(Text)
    quote = Column(String(2000))
    traits = relationship("Trait", cascade="all, delete")

    def replace_stats_in_string(self, dicestring):
        mid1 = dicestring.replace('str', "+" + str(self.str_base))
        mid2 = mid1.replace('def', "+" + str(self.def_base))
        mid3 = mid2.replace('mag', "+" +  str(self.mag_base))
        mid4 = mid3.replace('agi', "+" + str(self.agi_base))
        return mid4


def create_from_attribute_dict(attributes):
    character = Character()
    # TODO find a more secure way to give them IDs while still checking for duplicates
    #character.id = attributes.get('mun_id') + '.' + attributes.get('name')
    character.name = attributes.get('name')
    character.str_base = attributes.get('str_base')
    character.def_base = attributes.get('def_base')
    character.mag_base = attributes.get('mag_base')
    character.agi_base = attributes.get('agi_base')
    #TODO finish
    return character

def parse_attributes_from_txt(file_name):
    attribs = {}
    with open(file_name, "r") as infile:
        for line in infile:
            if line is "":
                continue
            split_line = line.strip().split('=')
            if len(split_line) is 1:
                attribs[split_line[0]] = None
            if len(split_line) is 2:
                attribs[split_line[0]] = split_line[1]
            else:
                return {}
    if 'name' not in attribs:
        return {}
    return attribs




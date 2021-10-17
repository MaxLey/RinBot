from sqlalchemy import Column, String, Text, ForeignKey, Integer

from models import Base


class StatObject(Base):

    __tablename__ = 'statobject'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'))

    str_base = Column(Integer)
    #str_finesse = Column(Integer)
    #str_knowledge = Column(Integer)
    #str_resolve = Column(Integer)
    #str_talent = Column(Integer)

    def_base = Column(Integer)
    #def_finesse = Column(Integer)
    #def_knowledge = Column(Integer)
    #def_resolve = Column(Integer)
    #def_talent = Column(Integer)

    agi_base = Column(Integer)
    #agi_finesse = Column(Integer)
    #agi_knowledge = Column(Integer)
    #agi_resolve = Column(Integer)
    #agi_talent = Column(Integer)

    mag_base = Column(Integer)
    #mag_finesse = Column(Integer)
    #mag_knowledge = Column(Integer)
    #mag_resolve = Column(Integer)
    #mag_talent = Column(Integer)


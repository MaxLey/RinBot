from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///testdb.db')
DBSessionMaker = sessionmaker(bind=engine)

def save(*args):
    with DBSessionMaker() as session:
        for object in args:
            session.merge(object) #TODO should this be merge?
        session.commit()

def get_by_id(object_class, object_id):
    with DBSessionMaker() as session:
        object = session.get(object_class, object_id)
    return object

# define your classes here like:
#class YourClassName(Base):
#    __tablename__ = 'your_table_name'
#    id = Column(Integer, primary_key=True)
#    number = Column(Integer)
#    name = Column(String(255))

# then connect to db
#engine = create_engine('sqlite:///webreader.db')
#DBSession = sessionmaker(bind=engine)
#session = DBSession()
#Base.metadata.bind = engine
#Base.metadata.create_all(engine)

# This is how you get all of them:
#def get_all() -> List[YourClassName]:
#    return session.query(YourClassName).all()
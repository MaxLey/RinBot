from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

import models.Ability
import models.Character
import models.Item
import models.StatObject
import models.Trait
import models.Mun

engine = create_engine('sqlite:///testdb.db')
Base.metadata.create_all(engine)
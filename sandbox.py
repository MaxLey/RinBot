import urllib.request

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import DiceHandler
from models.Character import Character
teststring = '3d6 +             +   1d20 + 2d6 -  3 + 7 - 3d7'
print(teststring)
testdict = DiceHandler.parse_dice_string(teststring)
print(testdict)

dicedict = {-6: 2}
result = DiceHandler.roll_dice_dict(dicedict)
print(result)

dicedict = {-6: 2}
result = DiceHandler.roll_dice_dict(testdict)
print(result)


#textfile_url = 'https://cdn.discordapp.com/attachments/885179213387276289/885794597605867540/template.txt'

#data = urllib.request.urlopen(textfile_url)
#for line in data:
#    print(line)

#engine = create_engine('sqlite:///testdb.db')

#connection = engine.connect()
#metadata = sa.MetaData()

#DBSession = sessionmaker(bind=engine)
#session = DBSession()

#mychar = Character()
#mychar.name = "Vani"
#session.merge(mychar)
#session.commit()

#mychar = [x for x in session.query(Character).filter_by(name='Vani')]
#print(mychar)

#print("===")
#print(session.query(Character).all())

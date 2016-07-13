from citadel_declarative import Base, User, Message
from sqlalchemy import create_engine
engine = create_engine('sqlite:///citadel_data.db')
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


def alc2json(row):
    return dict([(col, getattr(row,col)) for col in row.__table__.columns.keys()])

for user in session.query(User).all():
#	print user.userid + '(' + user.first_name + ' ' + user.last_name + ') '
#	print user.pw_hash
	print alc2json(user)

print 'total user count: ' + str(session.query(User).count())

for message in session.query(Message).all():
	print message.user.id
	print alc2json(message)
#	print user.title + ':'
#	print user.text
#	print 'from' + mesage.user[userid]
print 'total message count: ' + str(session.query(Message).count())




"""
print session.query(Message).filter(Message.user == user).all()

print session.query(Message).filter(Message.user == user).one()

message = session.query(Message).filter(Message.user == user).one()
print message.user_id
print message.title
print message.text
"""



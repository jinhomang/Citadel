from sqlalchemy_declarative import Base, User, Follower, Message
from sqlalchemy import create_engine
engine = create_engine('sqlite:///citadel_data.db')
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
session.query(User).all()


for user in session.query(User).all:
	print user.userid 
	print user.first_name + ' ' + user.last_name

"""
print session.query(Message).filter(Message.user == user).all()

print session.query(Message).filter(Message.user == user).one()

message = session.query(Message).filter(Message.user == user).one()
print message.user_id
print message.title
print message.text
"""



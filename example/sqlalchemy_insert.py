from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_declarative import User, Follower, Message, Base

engine = create_engine('sqlite:///sqlalchemy_example.db')


Base.metadata.bind = engine

DBsession = sessionmaker(bind = engine)

session = DBsession()

new_user = User(name = 'Jinho', email = 'jinhomang@gmail.com', pw_hash = '1234')
session.add(new_user)
session.commit()

new_message = Message(title='Test', text='This is a test')
session.add(new_message)
session.commit()


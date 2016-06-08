from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	userid = Column(String(250), nullable = False)
	first_name = Column(String(250), nullable = False)
	last_name = Column(String(250), nullable = False)
	email_addr = Column(String(250), nullable = False)
	nickname = Column(String(250), nullable = False)
	pw_hash = Column(String(250), nullable = False)

class Message(Base):
	__tablename__ = 'message'
	id = Column(Integer, primary_key = True)
	title = Column(String(250), nullable = False)
	text = Column(String(4096), nullable = False)

	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)


#engine = create_engine('sqlite:///citadel_data.db')

#Base.metadata.create_all(engine)


from sqlalchemy import Integer, SmallInteger, ForeignKey, String, String, UnicodeText, DateTime, Column, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(64), nullable=False) 
    name = Column(String(64), nullable=False)  
    password = Column(String(128), nullable=False)  #CHAR(128) NOT NULL,
    message_count = Column(SmallInteger)
    like_received = Column(SmallInteger)

    __table_args__ = (UniqueConstraint('user_id', name='_user_id_uc'), 
        UniqueConstraint('name', name='_name_uc'), 
        {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'})

    profile = relationship("Profile", back_populates='owner')
    messages = relationship("Message", back_populates='author')


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    picture = Column(String(256))
    url = Column(String(256)) 
    contact = Column(String(128)) 
    location = Column(String(128))
    bio = Column(String(256))  

    owner = relationship("Member", back_populates='profile')

    __table_args__ = (UniqueConstraint('owner_id', name='_owner_id_uc'), 
        {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'})


class Thread(Base):
    __tablename__='thread'
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    replies = Column(SmallInteger)
    views = Column(Integer)
    tags = Column(String(128))
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    messages = relationship("Message", back_populates='thread')


class Message(Base):
    __tablename__='message'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    thread_id = Column(Integer, ForeignKey('thread.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    content = Column(UnicodeText, nullable=False)

    thread = relationship("Thread", back_populates='messages')
    author = relationship("Member", back_populates='messages')

    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

engine = create_engine('mysql://root:jh781208@localhost/citadel', echo=True)
#engine = create_engine('sqlite:///citadel_data.db')
Base.metadata.create_all(engine)


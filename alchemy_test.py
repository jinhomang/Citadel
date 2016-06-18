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
    nickname = Column(String(32), nullable=False)  #CHAR(16) NOT NULL,
    password = Column(String(128), nullable=False)  #CHAR(128) NOT NULL,
    cgroup = Column(String(32), nullable=False)  
    message_count = Column(SmallInteger)
    like_received = Column(SmallInteger)
    trophy_point = Column(SmallInteger)
    homepage = Column(String(128))
    location = Column(String(64))
    occupation = Column(String(64))
    interact = Column(String(64))
    #__table_args__ = (UniqueConstraint('user_id', 'nickname', name='_user_nickname_uc'),)
    __table_args__ = (UniqueConstraint('user_id', name='_user_id_uc'), 
        UniqueConstraint('nickname', name='_nickname_uc'), 
        {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'})

    messages = relationship("Message", back_populates='author')

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
    thread_id = Column(Integer, ForeignKey('thread.id'))
    author_id = Column(Integer, ForeignKey('member.id'))
    content = Column(UnicodeText, nullable=False)

    thread = relationship("Thread", back_populates='messages')
    author = relationship("Member", back_populates='messages')

    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

engine = create_engine('mysql://root:jh781208@localhost/citadel', echo=True)
#engine = create_engine('sqlite:///citadel_data.db')
Base.metadata.create_all(engine)

"""
CREATE TABLE member (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    user_id VARCHAR(64) NOT NULL, 
    name VARCHAR(64) NOT NULL, 
    nickname VARCHAR(16) NOT NULL, 
    password VARCHAR(128) NOT NULL, 
    cgroup VARCHAR(32) NOT NULL, 
    message_count SMALLINT, 
    like_received SMALLINT, 
    trophy_point SMALLINT, 
    homepage VARCHAR(128), 
    location VARCHAR(64), 
    occupation VARCHAR(64), 
    interact VARCHAR(64), 
    PRIMARY KEY (id), 
    CONSTRAINT _user_id_uc UNIQUE (user_id), 
    CONSTRAINT _nickname_uc UNIQUE (nickname)
)ENGINE=InnoDB CHARSET=utf8


CREATE TABLE thread (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    title VARCHAR(256) NOT NULL, 
    replies SMALLINT, 
    views INTEGER, 
    tags VARCHAR(128), 
    PRIMARY KEY (id)
)ENGINE=InnoDB CHARSET=utf8


CREATE TABLE message (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    content TEXT NOT NULL, 
    date DATETIME NOT NULL, 
    thread_id INTEGER, 
    author_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(thread_id) REFERENCES member (id), 
    FOREIGN KEY(author_id) REFERENCES thread (id)
)ENGINE=InnoDB CHARSET=utf8
"""

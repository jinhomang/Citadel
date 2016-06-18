#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alchemy_test import Base, Message, Member, Thread 

engine = create_engine('mysql://root:jh781208@localhost/citadel?charset=utf8&use_unicode=0')

Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()


new_member = Member(
	user_id='a@gmail.com',
	name=u'김보람',
	nickname=u'그랑드',
	password='1234',
	cgroup='admin')
session.add(new_member)

new_member = Member(
	user_id='b@gmail.com',
	name=u'나선주',
	nickname=u'나잘남',
	password='1234',
	cgroup='admin')
session.add(new_member)

new_member = Member(
	user_id='c@gmail.com',
	name=u'다구리',
	nickname=u'다죽어',
	password='1234',
	cgroup='admin')
session.add(new_member)

new_member = Member(
	user_id='d@gmail.com',
	name=u'라미란',
	nickname='라디오',
	password='1234',
	cgroup='admin')
session.add(new_member)

session.commit()


new_thread = Thread(title='안녕하세요. 첫번째 쓰레드!')
session.add(new_thread)
new_thread = Thread(title='두번째 쓰레드입니다.')
session.add(new_thread)
new_thread = Thread(title='세번째 쓰레드입니다.')
session.add(new_thread)

session.commit()

new_message1_1 = Message(
	content=u'ㅋㅋㅋㅋㅋㅋ \n ㅋㅋㅋㅋㅋ',
	thread_id=1, 
	author_id=1,
	date='2016-06-17')
new_message1_2 = Message(
	content=u'하하하하하하 \n 흐흐흐흐흐',
	thread_id=1, 
	author_id=2,
	date='2016-06-17 00:00:00')
new_message2_1= Message(
	content=u'고고',
	thread_id=2, 
	author_id=1,
	date='2016-06-17 00:00:00')
new_message3_1= Message(
	content=u'뭐라는겨? \n 나도 몰라',
	thread_id=2, 
	author_id=3,
	date='2016-06-17 00:00:00')
new_message3_2= Message(
	content=u'혼날래? \n 뭐래니',
	thread_id=2, 
	author_id=3,
	date='2016-06-17 00:00:00')
session.add(new_message1_1)
session.add(new_message1_2)
session.add(new_message2_1)
session.add(new_message3_1)
session.add(new_message3_2)
session.commit()

#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from random import randrange;
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alchemy_test import Base, Message, Member, Thread 

engine = create_engine('mysql://root:jh781208@localhost/test?charset=utf8&use_unicode=0')

Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

"""
for idx in range(100):
	new_member = Member(
		user_id=str(idx) +'@mail.com',
		name='맹'+str(idx),
		nickname='매니아'+str(idx),
		password= str(idx) + '00',
		cgroup='admin',
   		message_count = 0,
    	like_received = 0,
    	trophy_point = 0)
	session.add(new_member)

session.commit()

for idx in range(100):
	new_thread = Thread(title='안녕하세요.'+ str(idx+1) + '번째 쓰레드!', replies=0, views=0)
	session.add(new_thread)

session.commit()
"""

for tc in range(100):
	first_message = Message(
			content= '이것은 쓰레드 첫번째 메시지입니다. \n 하하하 \n ㅋㅋㅋㅋㅋ \n ',
			thread_id=tc+101,
			author_id=randrange(1,101),
			date=datetime(year=2016, month=randrange(1,13), day=randrange(1,29), hour=randrange(0,24), minute=randrange(0,60)).strftime('%Y-%m-%d %H:%M:%S'))
	session.add(first_message)

	for mc in range(4):
			new_message = Message(
						content= '이것은 ' + str((tc*4)+(mc+1)) +'번째 생성된 랜덤 메시지입니다. \n 쿄쿄쿄쿄 \n ㅋㅋㅋㅋㅋ \n ',
						thread_id=randrange(101,201), 
						author_id=randrange(1,101),
						date=datetime(year=2016, month=randrange(1,13), day=randrange(1,29), hour=randrange(0,24), minute=randrange(0,60)).strftime('%Y-%m-%d %H:%M:%S'))
			session.add(new_message)
session.commit()
session.close()

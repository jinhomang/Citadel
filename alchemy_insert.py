#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from random import randrange;
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alchemy_citadel import Base, Profile, Message, Member, Thread 

engine = create_engine('mysql://root:jh781208@localhost/citadel?charset=utf8&use_unicode=0')

Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()


members = []
for idx in range(100):
	new_member = Member(
		user_id=str(idx) +'@mail.com',
		name='매니아'+str(idx),
		password= str(idx) + '00',
   		message_count = 0,
    	like_received = 0)
	session.add(new_member)
	members.append(new_member)

	profile = Profile()
	profile.picture = ""
	profile.url = ""
	profile.contact = ""
	profile.location = ""
	profile.bio = ""
	profile.owner = new_member
	session.add(profile)

mc = 0
threads = []
for idx in range(500):
	new_thread = Thread(title='안녕하세요.'+ str(idx+1) + '번째 쓰레드입니다!', replies=0, views=0)
	threads.append(new_thread)
	session.add(new_thread)

	first_message = Message();
	first_message.content = '이것은 커뮤니티 쓰레드 첫번째 메시지입니다. <br/> 하하하 <br/> ㅋㅋㅋㅋㅋ'
	first_message.date=datetime(year=2016, month=randrange(1,13), day=randrange(1,29), hour=randrange(0,24), minute=randrange(0,60)).strftime('%Y-%m-%d %H:%M:%S')
	first_message.author = members[randrange(0,len(members))]
	first_message.thread = new_thread
	session.add(first_message)

	for idx in range(randrange(0,12)):			
		mc+=1;
		new_message = Message()
		new_message.content= '이것은 ' + str(mc) +'번째 생성된 랜덤 메시지입니다. <br/> 쿄쿄쿄쿄 <br/> ㅋㅋㅋㅋㅋ',
		new_message.date=datetime(year=2016, month=randrange(1,13), day=randrange(1,29), hour=randrange(0,24), minute=randrange(0,60)).strftime('%Y-%m-%d %H:%M:%S')
		new_message.author = members[randrange(0,len(members))]
		new_message.thread = new_thread
		session.add(new_message)

session.commit()

session.close()

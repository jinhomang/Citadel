# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# All the importers #####################################################################
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash, session, abort
from wtforms import Form, TextField, BooleanField, PasswordField, \
HiddenField, SubmitField, TextAreaField, validators

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemy_test import Base, Member, Thread, Message

DEBUG = True
SECRET_KEY = 'development key'

# db ####################################################################################
engine = create_engine('mysql://root:jh781208@localhost/test?charset=utf8&use_unicode=0')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
dbs = DBsession()


# error messages ########################################################################
errorMsg = dict([('database_exception', '데이터베이스 오류가 발생했습니다: '),
			('user_id_duplicated', '동일한 아이디를 가진 사용자가 이미 존재합니다.'),
			('user_id_not_exists', '입력하신 아이디가 존재하지 않습니다.'),
			('wrong_password', '패스워드가 맞지 않습니다.'),
			('thread_not_exists', '해당 쓰레드는 존재하지 않습니다.'),
			('delete_message_error', '해당 글이 존재하지 않거나, 이 글을 삭제할 권한이 없습니다.')])


# Flask #################################################################################
app = Flask(__name__)
app.config.from_object(__name__)


# Forms #################################################################################
class RegistUserForm(Form):
	user_id = TextField('아이디', 
		[validators.Length(min=2, max=64), validators.Email()], 
		default = 'example@mail.com')
	name = TextField('이름', 
		[validators.Length(min=2, max=64)], 
		default ='홍길동')
	nickname = TextField('별명',
		[validators.Length(min=1, max=32)], 
		default='신출귀몰')
	password = PasswordField('패스워드',
		[validators.Length(min=6, max=128)])
	homepage = TextField('홈페이지',
    	[validators.Length(min=2, max=128), validators.URL()])
	location = TextField('지역',
    	[validators.Length(min=2, max=64)])
	occupation = TextField('직업',
    	[validators.Length(min=2, max=64)])
	interact = TextField('연락처', 
		[validators.Length(min=2, max=64)])
	submit = SubmitField('등록')
	accept_rules = BooleanField('약관 동의', 
		[validators.Required()])

class LoginForm(Form):
	user_id = TextField('아이디', 
		[validators.Length(min=2, max=64), validators.Email()])
	password = PasswordField('패스워드')
	submit = SubmitField('로그인')

class CreateThreadForm(Form):
	title = TextField('제목', [validators.Length(min=1, max=32)])
	content = TextAreaField('내용', [validators.Length(min=1)])
	submit = SubmitField('생성')

class AddMessageForm(Form):
	content = TextAreaField('댓글', [validators.Length(min=1)])
	submit = SubmitField('추가')	

class UpdatesMessageForm(Form):
	content = TextAreaField('내용', [validators.Length(min=1)])
	submit = SubmitField('수정')	


# Regist ################################################################################
@app.route('/regist_user', methods = ['GET', 'POST'])
def regist_user():
	error = None
	regist_form = RegistUserForm(request.form)
	if request.method == 'POST' and regist_form.validate():
		if dbs.query(Member).filter(Member.user_id == regist_form['user_id'].data).count() > 0:
			error = errorMsg['user_id_duplicated']
			dbs.close()
		else:
			try:
				new_member = Member(user_id=regist_form['user_id'].data,
								name=regist_form['name'].data,
								nickname=regist_form['nickname'].data,
								password=regist_form['password'].data,
								homepage=regist_form['homepage'].data,
								location=regist_form['location'].data,
								occupation=regist_form['occupation'].data,
								interact=regist_form['interact'].data,
								cgroup='관리자')
				dbs.add(new_member)
				dbs.commit()
			except Exception as e:
				error = errorMsg['database_exception'] + str(e)
				dbs.f()
				raise e
			else:				
				return redirect(url_for('main'))	
			finally: 
				dbs.close()
			
	else:
		return render_template('regist_user.html', form=regist_form, err=error)


# Login/Logout ##########################################################################
def alc2json(row):
    return dict([(col, getattr(row,col)) for col in row.__table__.columns.keys()])

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	login_form = LoginForm(request.form)
	if request.method == 'POST' and login_form.validate():
		q = dbs.query(Member).filter(Member.user_id == login_form['user_id'].data)
		if q.count() == 0:
			error = errorMsg['user_id_not_exists']
			dbs.close()
		else:
			user = q.one()
			dbs.close()

			if login_form['password'].data != user.password:
				error = errorMsg['wrong_password']
			else:
				session['user_info'] = alc2json(user)
				return redirect(url_for('main'))

	return render_template('login.html', form=login_form, err=error)

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('main'))


# Create thread #########################################################################
@app.route('/create_thread', methods = ['GET','POST'])
def create_thread():
	if not session.get('user_info'):
		abort(403)

	create_form = CreateThreadForm(request.form)
	if request.method == 'POST' and create_form.validate():
		try:
			new_thread = Thread()
			setattr(new_thread, 'title', create_form['title'].data)
			setattr(new_thread, 'views', 0)
			setattr(new_thread, 'replies', 0)			
			first_message = Message()
			setattr(first_message, 'content', create_form['content'].data)
			setattr(first_message, 'author_id', session['user_info']['id'])
			setattr(first_message, 'thread', new_thread)
			setattr(first_message, 'date', datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
			dbs.add(new_thread)
			dbs.add(first_message)
			dbs.commit()
		except Exception as e:
			error = errorMsg['database_exception'] + str(e)
			dbs.rollback()
			raise e
		else:
			return redirect(url_for('main'))
		finally: 
			dbs.close()

	else:
		return render_template('create_thread.html', form=create_form)


# Update thread #########################################################################
@app.route('/update_thread/<id>', methods = ['GET', 'POST'])
def delete_thread(id):
	pass


# Add message ###########################################################################
@app.route('/add_message/<thread_id>', methods = ['POST'])
def add_message(thread_id):
	if not session.get('user_info'):
		abort(403)

	reply_form = AddMessageForm(request.form)
	if reply_form.validate():
		try:
			new_message = Message()
			setattr(new_message, 'content', reply_form['content'].data)
			setattr(new_message, 'author_id', session['user_info']['id'])
			setattr(new_message, 'thread_id', thread_id)
			setattr(new_message, 'date',  datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
			dbs.add(new_message)
			dbs.commit()
		except Exception as e:
			error = errorMsg['database_exception'] + str(e)
			dbs.rollback()
			raise e
		finally: 
			dbs.close()

		
	return redirect(url_for('show_thread', id=thread_id))


# Update message ########################################################################
@app.route('/update_message/<thread_id>/<message_id>', methods = ['GET', 'POST'])
def update_message(thread_id, message_id):
	if not session.get('user_info'):
		abort(403)

	message_form = UpdatesMessageForm(request.form)
	if request.method == 'POST' and message_form.validate():
		try:
			updated_message = dbs.query(Message).filter(Message.id == message_id).filter(Message.author_id == session['user_info']['id']).one()
			setattr(updated_message, 'content', message_form['content'].data)
			setattr(updated_message, 'date',  datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
			dbs.add(updated_message)
			dbs.commit()
		except Exception as e:
			error = errorMsg['database_exception'] + str(e)
			dbs.rollback()
			raise e
		else:
			return redirect(url_for('show_thread', id=thread_id))
		finally: 
			dbs.close()
	else:
		message = dbs.query(Message).filter(Message.id == message_id).one()
		dbs.close()

		message_form['content'].data = message.content;

		return render_template('update_message.html', form=message_form, thread_id=thread_id, message_id=message_id)


# Delete message ########################################################################
@app.route('/delete_message/<thread_id>/<message_id>')
def delete_message(thread_id, message_id):
	if not session.get('user_info'):
		abort(403) 

	try:
		q = dbs.query(Message).filter(Message.id == message_id and Message.author_id == session['user_info']['id'])
		if q.count() == 0:
			error = errorMsg['delete_message_error'] 
		else:
			dbs.delete(q.one())
			dbs.commit()
	except Exception as e:
		error = errorMsg['database_exception'] + str(e)	
		dbs.rollback()
		raise e
	finally: 
		dbs.close()

		
	return redirect(url_for('show_thread', id=thread_id))	


# Show thread ###########################################################################
@app.route('/thread/<id>')
def show_thread(id):
	error = None
	q = dbs.query(Thread).filter(Thread.id == id)
	dbs.close()

	if q.count() == 0:
		error = errorMsg['thread_not_exists']
	else:
		thread = alc2json(q.one())
		messages = [(alc2json(msg), alc2json(msg.author)) for msg in q.one().messages]
		message_form = AddMessageForm(request.form)	
		return render_template('show_thread.html', thread=thread, messages=messages, form=message_form)	

	return redirect('main')


# Show thread list ######################################################################
@app.route('/forums/<name>')
def forum(name):
	q = dbs.query(Thread).all()
	threads = [(alc2json(thread), alc2json(thread.messages[0]), alc2json(thread.messages[0].author)) for thread in q]
	dbs.close()

	return render_template('forum.html', name=name, threads=threads)


# Main ##################################################################################
@app.route('/')
def main():
	return redirect(url_for('forum', name='unity'))

# run the application
if __name__ == '__main__':
	app.run()


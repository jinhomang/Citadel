# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# All the importers #####################################################################
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash, session, abort
from wtforms import Form, TextField, BooleanField, PasswordField, \
HiddenField, SubmitField, TextAreaField, validators

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from alchemy_citadel import Base, Member, Profile, Thread, Message

from flask_util_js import FlaskUtilJs

DEBUG = True
SECRET_KEY = 'development key'

# db ####################################################################################
engine = create_engine('mysql://root:jh781208@localhost/citadel?charset=utf8&use_unicode=0')
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

# FlaskUtilJs ###########################################################################
fujs = FlaskUtilJs(app)
@app.context_processor
def inject_fujs():
	return dict(fujs=fujs)

# Forms #################################################################################

user_id_validators = [validators.Length(min=2, max=64), validators.Email()]
user_name_validators = [validators.Length(min=2, max=64)]
password_validators = [validators.Length(min=6, max=128)]

class JoinForm(Form):
	user_id = TextField('이메일 주소', user_id_validators)
	name = TextField('이름', user_name_validators)
	password = PasswordField('패스워드', password_validators)
	submit = SubmitField('가입하기')

class ProfileForm(Form):
	name = TextField('이름', user_name_validators)
	bio = TextAreaField('바이오그래피', [validators.Length(max=256)])
	url = TextField('URL', [validators.Length(max=128), validators.URL()])
	contact = TextField('연락처', [validators.Length(max=32)])
	location = TextField('지역', [validators.Length(max=32)])
	picture = TextField('사진', [validators.Length(max=128)])
	# submit = SubmitField('수정완료')

class UpdatePasswordForm(Form):
	new_password = PasswordField('새로운 패스워드', password_validators)
	confirm_password = PasswordField('패스워드 재입력')

class LoginForm(Form):
	user_id = TextField('이메일')
	password = PasswordField('패스워드')
	submit = SubmitField('로그인')

# class CreateThreadForm(Form):
# 	title = TextField('제목', [validators.Length(min=1, max=32)])
# 	content = TextAreaField('내용', [validators.Length(min=1)])
# 	submit = SubmitField('생성')

# class AddMessageForm(Form):
# 	content = TextAreaField('댓글', [validators.Length(min=1)])
# 	submit = SubmitField('추가')	

# class UpdatesMessageForm(Form):
# 	content = TextAreaField('내용', [validators.Length(min=1)])
# 	submit = SubmitField('수정')	

#########################################################################################
# @app.teardown_request
# def session_clear(exception=None):
#     session.remove()
#     if exception and session.is_active:
#         session.rollback()

# FB ####################################################################################
@app.route('/fb_test')
def fb_test():
	return render_template('fb_test.html')

# Regist ################################################################################
# @app.route('/regist_user', methods = ['GET', 'POST'])
# def regist_user():
# 	error = None
# 	regist_form = RegistUserForm(request.form)
# 	if request.method == 'POST' and regist_form.validate():
# 		if dbs.query(Member).filter(Member.user_id == regist_form['user_id'].data).count() > 0:
# 			error = errorMsg['user_id_duplicated']
# 			dbs.close()
# 		else:
# 			try:
# 				new_member = Member(user_id=regist_form['user_id'].data,
# 								name=regist_form['name'].data,
# 								nickname=regist_form['nickname'].data,
# 								password=regist_form['password'].data,
# 								homepage=regist_form['homepage'].data,
# 								location=regist_form['location'].data,
# 								occupation=regist_form['occupation'].data,
# 								interact=regist_form['interact'].data,
# 								cgroup='관리자')
# 				dbs.add(new_member)
# 				dbs.commit()
# 			except Exception as e:
# 				error = errorMsg['database_exception'] + str(e)
# 				dbs.f()
# 				raise e
# 			else:				
# 				return redirect(url_for('main'))	
# 			finally: 
# 				dbs.close()
			
# 	else:
# 		return render_template('regist_user.html', form=regist_form, err=error)
@app.route('/join', methods = ['GET', 'POST'])
def join():
	if session.get('user_info'):
		return redirect( url_for('main'))

	error = None
	regist_form = JoinForm(request.form)
	if request.method == 'POST' and regist_form.validate():
		if dbs.query(Member).filter(Member.user_id == regist_form['user_id'].data).count() > 0:
			error = errorMsg['user_id_duplicated']
			dbs.close()
		else:
			try:
				new_member = Member(
								user_id=regist_form['user_id'].data,
								name=regist_form['name'].data,
								nickname=regist_form['name'].data,
								password=regist_form['password'].data,
								cgroup='관리자')
				new_member.profile = Profile()
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
			
	return render_template('join.html', form=regist_form, err=error)



# Login/Logout ##########################################################################
def alc2json(row):
    return dict([(col, getattr(row,col)) for col in row.__table__.columns.keys()])

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if session.get('user_info'):
		return redirect( url_for('main'))

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


# View profile ##########################################################################
@app.route('/profile')
def profile():
	if not session.get('user_info'):
		return redirect(url_for('main'))

	user = dbs.query(Member).filter(Member.id == session['user_info']['id']).one()
	session['user_info'] = alc2json(user)

	profile = alc2json(dbs.query(Profile).filter(Profile.owner_id == session['user_info']['id']).one())
	dbs.close()

	return render_template('profile.html', profile=profile)


# Edit profile ##########################################################################
@app.route('/edit_profile', methods = ['GET', 'POST'])
def edit_profile():
	if not session.get('user_info'):
		return redirect(url_for('main'))

	form = ProfileForm(request.form)
	if request.method == 'POST':	
		try:
			# session['user_info'].name = form['name'].data
			updated_profile = dbs.query(Profile).filter(Profile.owner_id == session['user_info']['id']).one()
			updated_profile.picture = form['picture'].data
			updated_profile.url = form['url'].data
			updated_profile.contact = form['contact'].data
			updated_profile.location = form['location'].data
			updated_profile.bio = form['bio'].data

			dbs.add(updated_profile)
			dbs.commit()
		except Exception as e:
			error = errorMsg['database_exception'] + str(e)
			dbs.rollback()
			raise e
		else:
			return redirect(url_for('profile'))
		finally: 
			dbs.close()
	else:
		profile = alc2json(dbs.query(Profile).filter(Profile.owner_id == session['user_info']['id']).one())
		dbs.close()
		
	return render_template('edit_profile.html', form=form, profile=profile)


# Create thread #########################################################################
@app.route('/create_thread', methods = ['GET','POST'])
def create_thread():
	if not session.get('user_info'):
		abort(403)

	if request.method == 'POST':
		try:
			new_thread = Thread()
			setattr(new_thread, 'title', request.form['ed_title'])
			setattr(new_thread, 'views', 0)
			setattr(new_thread, 'replies', 0)			

			first_message = Message()
			first_message.thread = new_thread;
			first_message.author = dbs.query(Member).filter(session['user_info']['id'] == Member.id).one()
			first_message.author.message_count +=1
			first_message.content = request.form['content']
			first_message.date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

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
		return render_template('create_thread.html')


# Update thread #########################################################################
# @app.route('/delete_thread/<id>', methods = ['GET', 'POST'])
# def delete_thread(id):
# 	pass


# Add message ###########################################################################
@app.route('/add_message/<thread_id>', methods = ['POST'])
def add_message(thread_id):
	if not session.get('user_info'):
		abort(403)

	try:
		new_message = Message()
		new_message.content = request.form['content']
		new_message.date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		new_message.thread = dbs.query(Thread).filter(Thread.id == thread_id).one()
		new_message.thread.replies +=1 #len(new_message.thread.messages)
		new_message.author = dbs.query(Member).filter(session['user_info']['id'] == Member.id).one()
		new_message.author.message_count +=1

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

	if request.method == 'POST':
		try:
			updated_message = dbs.query(Message).filter(Message.id == message_id).filter(Message.author_id == session['user_info']['id']).one()
			setattr(updated_message, 'content', request.form['content'])
			setattr(updated_message, 'date', datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
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
		thread = alc2json(message.thread)
		dbs.close()
		return render_template('update_message.html', thread=thread, message_id=message_id, content=message.content)



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
			message = q.one()
			message.thread.replies = max(0, message.thread.replies - 1) #len(new_message.thread.messages)
			message.author.message_count = max(0, message.author.message_count - 1)
			dbs.delete(message)
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

	if q.count() == 0:
		error = errorMsg['thread_not_exists']
		dbs.close()
	else:
		this_thread = q.one();

		thread = alc2json(this_thread)
		messages = [(alc2json(msg), alc2json(msg.author)) for msg in this_thread.messages]
		# message_form = AddMessageForm(request.form)
		dbs.close()

		return render_template('show_thread.html', thread=thread, messages=messages)#, form=message_form)	

	return redirect('main')


# Show thread list ######################################################################
@app.route('/forums/<name>/<page>')
def forum(name, page):

	# total_rows: 현재 게시판의 전체 쓰레드 행 개수
	# page_rows: 한 페이지에 출력되는 쓰레드 행 개수
	# cur_page_idx: 현재 보여지는 페이지의 인덱스
	# first_row_idx: 현재 보여지는 페이지의 첫번째 쓰레드 행 인덱스 
	# last_row_idx:  현재 보여지는 페이지의 마지막 쓰레드 행 인덱스 

	total_rows = len(dbs.query(Thread).all())
	page_rows = 20 
	total_pages = total_rows / page_rows
	if (total_rows%page_rows) > 0:
		total_pages += 1

	cur_page_idx = min(int(page)-1, max(0, total_pages-1))
	first_row_idx = cur_page_idx * page_rows
	last_row_idx = min(first_row_idx + page_rows, total_rows)
	q = dbs.query(Thread).order_by(desc(Thread.id))[first_row_idx : last_row_idx]
	threads = [(alc2json(thread), alc2json(thread.messages[0]), alc2json(thread.messages[0].author)) for thread in q]

	dbs.close()

	max_page_display = 10
	start_page_idx = (cur_page_idx / max_page_display) * max_page_display
	end_page_idx = min(start_page_idx + max_page_display, total_pages)

	return render_template('forum.html', 
							name=name, 
							threads=threads, 
							total_pages=total_pages, 
							start_page_idx=start_page_idx,
							end_page_idx=end_page_idx, cur_page_idx=cur_page_idx)

@app.route('/editor')
def editor():
	return render_template('editor.html')

# Main ##################################################################################
@app.route('/')
def main():
	return redirect(url_for('forum', name='unity', page=1))

# run the application
if __name__ == '__main__':
	app.run()


# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# All the importers #####################################################################
from flask import Flask, request, redirect, url_for, render_template, flash, session, abort
from wtforms import Form, TextField, BooleanField, PasswordField, \
HiddenField, SubmitField, TextAreaField, validators

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemy_test import Base, Member, Thread, Message

DEBUG = True
SECRET_KEY = 'development key'

# db ####################################################################################
engine = create_engine('mysql://root:jh781208@localhost/citadel?charset=utf8&use_unicode=0')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
dbs = DBsession();


# Flask #################################################################################
app = Flask(__name__)
app.config.from_object(__name__)


# Regist ################################################################################
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

@app.route('/regist_user', methods = ['GET', 'POST'])
def regist_user():
	error = None
	regist_form = RegistUserForm(request.form)
	if request.method == 'POST' and regist_form.validate():
		if dbs.query(Member).filter(Member.user_id == regist_form['user_id'].data).count() > 0:
			error = '동일한 아이디를 가진 사용자가 이미 존재합니다.'
		else:
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
			return redirect(url_for('main'))	

	return render_template('regist_user.html', form=regist_form, err=error)


# Login/Logout ##########################################################################
class LoginForm(Form):
	user_id = TextField('아이디', 
		[validators.Length(min=2, max=64), validators.Email()])
	password = PasswordField('패스워드')
	submit = SubmitField('로그인')

def alc2json(row):
    return dict([(col, getattr(row,col)) for col in row.__table__.columns.keys()])

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	login_form = LoginForm(request.form)
	if request.method == 'POST' and login_form.validate():
		q = dbs.query(Member).filter(Member.user_id == login_form['user_id'].data)
		if q.count() == 0:
			error = '입력하신 아이디가 존재하지 않습니다.'
		else:
			user = q.one()
			if login_form['password'].data != user.password:
				error = '패스워드가 맞지 않습니다.'
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
	pass


# Update thread #########################################################################
@app.route('/update_thread/<id>', methods = ['GET', 'POST'])
def delete_thread(id):
	pass


# Add message ###########################################################################
@app.route('/add_message/<thread_id>/message_id', methods = ['GET', 'POST'])
def add_message(thread_id, message_id):
	pass	


# Update message ########################################################################
@app.route('/update_message/<thread_id>/<message_id>', methods = ['GET', 'POST'])
def update_message(thread_id, message_id):
	pass


# Delete message ########################################################################
@app.route('/delete_message/<thread_id>/<message_id>')
def delete_message(thread_id, message_id):
	pass


# Show thread ###########################################################################
@app.route('/thread/<id>')
def show_thread(id):
	error = None
	q = dbs.query(Thread).filter(Thread.id == id)
	if q.count() == 0:
		error = '해당 쓰레드는 존재하지 않습니다.'
	else:
		thread = alc2json(q.one())
		messages = [alc2json(msg) for msg in q.one().messages] 
		return render_template('show_thread.html', thread=thread, messages=messages)	
			
	return redirect('main')


# Show thread list ######################################################################
def alc2jsonex(row):
    return dict([(col, getattr(row, col)) for col in row.__table__.columns.keys()] + [('author_name', row.messages[0].author.nickname)])
@app.route('/forums/<name>')
def forum(name):
	threads = [alc2jsonex(thread) for thread in dbs.query(Thread).all()]
	return render_template('forum.html', name=name, threads=threads)


# Main ##################################################################################
@app.route('/')
def main():
	return redirect(url_for('forum', name='unity'))

# run the application
if __name__ == '__main__':
	app.run()


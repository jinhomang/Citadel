############################################################
# All the importers
from flask import Flask, request, redirect, url_for, render_template, flash, session, abort
from wtforms import Form, TextField, BooleanField, PasswordField, \
HiddenField, SubmitField, TextAreaField, validators

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from citadel_declarative import Base, User, Message

DEBUG = True
SECRET_KEY = 'development key'

############################################################
# DB
engine = create_engine('sqlite:////Users/jinho/Citadel/citadel_data.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
dbs = DBsession();

############################################################
# app
app = Flask(__name__)
app.config.from_object(__name__)


############################################################
# test page
@app.route('/ok')
def ok():
	return render_template('test.html')


############################################################
# register
class RegistUserForm(Form):
	userid = TextField('ID', [validators.Length(min=4, max=25)], default = 'jinhomang')
	firstname = TextField('first name', [validators.Length(min=2, max=25)], default = 'Jinho')
	lastname = TextField('last name', [validators.Length(min=2, max=35)], default = 'Mang')
	nickname = TextField('nickname', [validators.Length(min=3, max=50)], default = 'Black Knight')
	password = PasswordField('password')
	emailaddr = TextField('email address', 
				[validators.Length(min=6, max=50), validators.Email()], 
				default = 'jinho@gmail.com')
	accept_rules = BooleanField('accept rules', [validators.Required()])
	submit = SubmitField('register')

@app.route('/regist_user', methods = ['GET', 'POST'])
def regist_user():
	error = None
	form = RegistUserForm(request.form)
	if request.method == 'POST' and form.validate():
		#	check new user duplicated in database
		if dbs.query(User).filter(User.userid == form['userid'].data).count() > 0:
			error = 'Same ID already exists'
		else:
			#	insert new user into database
			new_user = User(userid = form['userid'].data,
							first_name = form['firstname'].data,
							last_name = form['lastname'].data,
							email_addr = form['emailaddr'].data,
							nickname = form['nickname'].data,
							pw_hash = form['password'].data)
							
			dbs.add(new_user)
			dbs.commit()
			return redirect(url_for('main'))	

	return render_template('regist_user.html', form=form, err=error)


############################################################
# unregister
@app.route('/unregist_user', methods = ['GET', 'POST'])
def unregist_user():
	pass


############################################################
# login
class LoginForm(Form):
	userid = TextField('ID', [validators.Length(min=4, max=25)], default = 'jinhomang')
	password = PasswordField('password')
	submit = SubmitField('login')

def alc2json(row):
    return dict([(col, getattr(row,col)) for col in row.__table__.columns.keys()])


@app.route('/login', methods = ['GET', 'POST'])
def log_in():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		#	check if user is registerd in database and paword is correct
		q = dbs.query(User).filter(User.userid == form['userid'].data)
		if q.count() == 0:
			error = 'ID doesn\'t exist'
		else:
			user = q.one()
			if form['password'].data != user.pw_hash:
				error = 'Password error'
			else:
				session['user_info'] = alc2json(user)
				return redirect(url_for('main'))	
			
	return render_template('login.html', form=form, err=error)


############################################################
# logout
@app.route('/logout', methods = ['GET', 'POST'])
def log_out():
	session.clear()
	return redirect(url_for('main'))


############################################################
# add post
class AddPostForm(Form):
	title = TextField('title', [validators.Length(min=1, max=32)])
	text = TextAreaField('content', [validators.Length(min=1, max=2048)])
	submit = SubmitField('add')


@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
	if not session.get('user_info'):
		abort(403)

	form = AddPostForm(request.form)
	if form.validate():
		new_post = Message()
		setattr(new_post, 'title', form['title'].data)
		setattr(new_post, 'text', form['text'].data)
		setattr(new_post, 'user_id', session['user_info']['id'])									
		dbs.add(new_post)
		dbs.commit()		
		return redirect(url_for('main'))
			
	return render_template('add_post.html', form=form)


############################################################
# delet post
@app.route('/delete_post/<id>')
def delete_post(id):
	if not session.get('user_info'):
		abort(403) 

	q = dbs.query(Message).filter(Message.id == id and Message.user_id == session['user_info']['id'])
	if q.count() == 0:
		error = 'the post does not exist'
	else:
		dbs.delete(q.one())
		dbs.commit()
		return redirect(url_for('main'))
		
	return redirect(url_for('main'))


############################################################
# update post
class UpdatePostForm(Form):
	title = TextField('title', [validators.Length(min=1, max=32)])
	text = TextAreaField('content', [validators.Length(min=1, max=2048)])
	submit = SubmitField('update')


@app.route('/update_post/<id>', methods = ['GET', 'POST'])
def update_post(id):
	if not session.get('user_info'):
		abort(403)

	form = UpdatePostForm(request.form)
	if request.method == 'POST':
		if form.validate():
			updated_post = dbs.query(Message).filter(
				Message.id == id).filter(
				Message.user_id == session['user_info']['id']).one()

			setattr(updated_post, 'title', form['title'].data)
			setattr(updated_post, 'text', form['text'].data)
			dbs.commit()
			return redirect(url_for('main'))

	post = dbs.query(Message).filter(Message.id == id).one()
	form['title'].data = post.title;
	form['text'].data = post.text;	
	return render_template('update_post.html', form=form, id=id)




############################################################
# show post
@app.route('/show_post/<id>')
def show_post(id):
	error = None
	q = dbs.query(Message).filter(Message.id == id)
	if q.count() == 0:
		error = 'the post does not exist'
	else:
		post = alc2json(q.one())
		return render_template('show_post.html', post=post)	
			
	return redirect('main')


############################################################
# show postlist
@app.route('/show_postlist')
def show_posts():
	return redirect(url_for('main'))
	

############################################################
# main
def alc2jsonex(row):
    return dict([(col, getattr(row,col)) for col in row.__table__.columns.keys()] + [('author', row.user.nickname)])

@app.route('/')
def main():	
	posts = [alc2jsonex(post) for post in dbs.query(Message).all()]

	if session.get('user_info'):
		form = AddPostForm(request.form)
		return render_template('main.html', form=form, posts=posts)

	return render_template('main.html', posts=posts)


############################################################
# edit a profile
class UpdateUserForm(Form):
	pass

@app.route('/update_profile', methods = ['GET', 'POST'])
def update_profile():
	pass


############################################################
# run the application
if __name__ == '__main__':
	app.run()



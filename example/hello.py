from flask import render_template, redirect, url_for

from flask import Flask 
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Jinho, Hello World!'

@app.route('/post')
def test_post():
	return 'adfadfasdfPost'

@app.route('/post/no<int:post_id>')
def show_post(post_id):
	return 'post %d' % post_id

@app.route('/memo')
def show_memo():
	return 'MEMO'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/tbd')
def tbd():
	return 'TBD...'

@app.route('/board')
def board():
	return redirect(url_for('tbd'))

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__=='__main__':
	app.run(debug=True)


	
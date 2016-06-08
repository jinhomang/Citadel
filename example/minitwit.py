#configuration
DATABASE = '/tmp/minitwit.db'
DEBUG = True


from flask import Flask 
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envar('MINITWIT_SETTINGS', silent=True)



from sqlite import dbapi2 as sqlite3
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


def initdb():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()



if __name__ == '__main__':
	app.run()


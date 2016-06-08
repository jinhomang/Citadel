############################################################
# All the importers
from flask import Flask, request, redirect, url_for, render_template, flash, session, abort

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def ok():
	return ('Hello Fucking WSGI and Apache')

############################################################
# run the application
if __name__ == '__main__':
	app.run()
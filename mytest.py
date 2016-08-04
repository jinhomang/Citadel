# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# All the importers #####################################################################
from flask import Flask, request, redirect, url_for, make_response, render_template, flash, session, abort

DEBUG = True
SECRET_KEY = 'development key'


# Flask #################################################################################
app = Flask(__name__)
app.config.from_object(__name__)


# FB ####################################################################################
@app.route('/hello')
def sayhello():
	return '<h1>Hello Flask, Hello Heroku!!!</h1>'

# main ##################################################################################
@app.route('/')
def main():
	return '<h1>This is my heroku test. <br/>이것은 헤로쿠 테스트입니다.</h1>'


# run the application  ##################################################################
if __name__ == '__main__':
	app.run()

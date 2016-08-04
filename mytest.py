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

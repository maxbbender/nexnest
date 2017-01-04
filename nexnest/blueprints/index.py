from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify

# from nexnest.application import session

indexs = Blueprint('indexs', __name__, template_folder='../templates')

@indexs.route('/')
@indexs.route('/index')
def index():
	return render_template('index.html')
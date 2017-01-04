from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify

# from nexnest.application import session

tests = Blueprint('tests', __name__, template_folder='../templates')

@tests.route('/test')
def test():
	return render_template('test.html')
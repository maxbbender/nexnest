from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.loginForm import LoginForm

from flask.ext.security import login_required
# from nexnest.application import session

indexs = Blueprint('indexs', __name__, template_folder='../templates')

# @indexs.route('/')
# @indexs.route('/index')
# def index():
#   form = LoginForm(request.form)
#   if request.method == 'POST' and form.validate():
#       #user = User(form.username.data, form.email.data,
#       #            form.password.data)
#       #db_session.add(user)
#       flash('Login Successfull')
#       return redirect(url_for('indexs.index'))
#   return render_template('index.html', form=form, title='NexNest')


@indexs.route('/test')
@login_required
def test():
    return render_template('test.html')

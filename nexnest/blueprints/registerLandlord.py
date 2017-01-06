from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.registrationLandlordForm import RegistrationLandlordForm

# from nexnest.application import session

registerLandlords = Blueprint('registerLandlords', __name__, template_folder='../templates')

@registerLandlords.route('/registerLandlord', methods=['GET', 'POST'])
def registerLandlord():
    form = RegistrationLandlordForm(request.form)
    if request.method == 'POST' and form.validate():
        #user = User(form.username.data, form.email.data,
        #            form.password.data)
        #db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('indexs.index'))
    return render_template('registerLandlord.html', form=form, title='Sign-Up')
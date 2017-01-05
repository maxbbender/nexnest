from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.registrationTenantForm import RegistrationTenantForm

# from nexnest.application import session

registerTenants = Blueprint('registerTenants', __name__, template_folder='../templates')

@registerTenants.route('/registerTenant', methods=['GET', 'POST'])
def registerTenant():
    form = RegistrationTenantForm(request.form)
    if request.method == 'POST' and form.validate():
        #user = User(form.username.data, form.email.data,
        #            form.password.data)
        #db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('indexs.index'))
    return render_template('registerTenant.html', form=form, title='Sign-Up')
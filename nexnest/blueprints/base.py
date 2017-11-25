from pprint import pformat

from flask import current_app as app
from flask import Blueprint, flash, render_template, send_from_directory
from flask_login import current_user, login_required

from nexnest.forms import ContactForm
from nexnest.utils.email import send_email
from nexnest.utils.flash import flash_errors

base = Blueprint('base', __name__, template_folder='../templates/base')


@base.route('/uploads/<path:path>')
def serve_upload(path):
    # print(path)
    return send_from_directory('uploads/', path)


@base.route('/contactUs', methods=['POST'])
def contactUs():
    form = ContactForm()

    if form.validate():
        htmlResponse = '''
            <h1>NEW CONTACT FORM AHHHHHHHHHHHHHHHHHHHHHHHHH</h1>
            Full Name Proivded: %s<br>
            Phone Number: %s<br>
            Message: %s<br>
            Email: %s
            ''' % (form.name.data, form.phone.data, form.message.data, form.email.data)

        if current_user.is_authenticated:
            htmlResponse += '''
            <br><br><br><hr>
            <h3>User Dump</h3>
            %s
            ''' % pformat(current_user.serialize)

        send_email(subject='Contact Us Form',
                   sender='no_reply@nexnest.com',
                   recipients=['contact@nexnest.com'],
                   html_body=htmlResponse)
        flash('Thank you for contacting Nexnest, we will address your issue and get back to you as soon as possible', 'success')
    else:
        flash_errors(form)

    return form.redirect()


@base.route('/promos/sale30', methods=['GET'])
def sale30():
    return render_template('promos/sale30.html',
                           title='Promo!')


@base.route('/debug')
def debug():
    app.logger.debug('Tetso')
    return 'hey'

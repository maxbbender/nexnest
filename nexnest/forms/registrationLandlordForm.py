from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationLandlordForm(Form): 
    fname = StringField('First Name', [validators.Length(min=1, max=25)])
    lname = StringField('Last Name', [validators.Length(min=1, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    numProperties = StringField('Number of Properties', [validators.Length(min=1, max=4), validators.DataRequired()])
    accept_emails = BooleanField('Recive email notifications', [validators.DataRequired()])
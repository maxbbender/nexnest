from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, Length

schools = [
  ('0', 'SUNY Fredonia')
]

class EditAccountForm(FlaskForm):
    fname = StringField('First Name', [InputRequired()])
    lname = StringField('Last Name', [InputRequired()])
    school = SelectField('School Attending', choices=schools)
    dob = StringField('Date of Birth')
    bio  = TextAreaField('If you wish provide a short personal bio')
    phone  = StringField('Phone Number', [Length(min=10, max=10)])
    website  = StringField('Your personal website url')
    email = StringField('Email',
                        [InputRequired("You must enter an email address"),
                         Email("Email must be valid format")])
    password = PasswordField('Change Password', [EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Confirm Password')

    
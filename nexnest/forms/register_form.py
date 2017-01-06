from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        [InputRequired("You must enter an email address"),
                         Email("Email must be valid format")])
    password = PasswordField('Password',
                             [InputRequired(),
                              EqualTo('confirm',
                                      message="Passwords must match")])
    confirm = PasswordField('Confirm Password', [InputRequired()])

    name = StringField('Name', [InputRequired()])
    submit = SubmitField('Register')

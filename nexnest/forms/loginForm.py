from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])

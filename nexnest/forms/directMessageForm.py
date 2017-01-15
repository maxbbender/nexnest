from flask_wtf import FlaskForm

from wtforms import TextAreaField, HiddenField

from wtforms.validators import InputRequired


class DirectMessageForm(FlaskForm):
    target_user_id = HiddenField('Target User', [InputRequired()])
    content = TextAreaField('Message', [InputRequired("Message is required")])

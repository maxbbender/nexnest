from flask_wtf import FlaskForm

from wtforms.fields import TextAreaField, HiddenField

from wtforms.validators import InputRequired


class TourMessageForm(FlaskForm):
    tour_id = HiddenField(
        'Tour ID', [InputRequired("Group ID Field Required")])
    content = TextAreaField(
        'Message', [InputRequired("You must put in a message")])

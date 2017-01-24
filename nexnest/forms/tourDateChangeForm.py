from flask_wtf import FlaskForm

from wtforms.fields import HiddenField, DateTime

from wtforms.validators import InputRequired, Length


class TourDateChangeForm(FlaskForm):
    input_id = HiddenField('group_id', [InputRequired()])
    requestedDateTime = HiddenField('Date and time you would like to tour the house')

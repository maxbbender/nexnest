from flask_wtf import FlaskForm

from wtforms.fields import TextAreaField, HiddenField, DateTimeField

from wtforms.validators import InputRequired


class TourForm(FlaskForm):
    listing_id = HiddenField('Listing ID', validators=[InputRequired()])
    group_id = HiddenField('Group ID', validators=[InputRequired()])
    time_requested = DateTimeField(
        'Requested Tour Time', validators=[InputRequired()])
    description = TextAreaField('Tour Request Message')

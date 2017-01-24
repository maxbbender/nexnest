from flask_wtf import FlaskForm

from wtforms.fields import HiddenField, StringField, TextAreaField

from wtforms.validators import InputRequired, Length


class TourForm(FlaskForm):
    group_id = HiddenField('group_id', [InputRequired()])
    listing_id = HiddenField('listing_id', [InputRequired()])
    description = TextAreaField('Message to Landlord', [Length(min=1, max=1500), InputRequired()])
    requestedDateTime = HiddenField('Date and time you would like to tour the house')

from flask_wtf import FlaskForm

from wtforms.fields import HiddenField

from wtforms.validators import InputRequired


class SuggestListingForm(FlaskForm):
    group_id = HiddenField('group_id', [InputRequired()])
    listing_id = HiddenField('listing_id', [InputRequired()])

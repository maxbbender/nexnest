from flask_wtf import FlaskForm

from wtforms.fields import HiddenField

from wtforms.validators import InputRequired


class InviteGroupForm(FlaskForm):
    group_id = HiddenField('group_id', [InputRequired()])
    user_id = HiddenField('user_id', [InputRequired()])

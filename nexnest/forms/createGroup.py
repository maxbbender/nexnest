from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField, DateField
from wtforms.validators import InputRequired, Email, EqualTo, Length

valid_time_frames = [
    ('0', '2017-2018 School Year'),
    ('1', '2018 Summer'),
    ('2', '2018-2019 School Year'),
    ('3', '2019 Summer')
]


class CreateGroupForm(FlaskForm):
    name = StringField('Group Name:', [Length(min=2, max=50), InputRequired()])
    # time_frame = SelectField(
    #     'When are you looking for a house?', choices=valid_time_frames)
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')

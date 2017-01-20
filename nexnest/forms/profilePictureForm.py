from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class ProfilePictureForm(FlaskForm):
    profilePicture = FileField('Profile Picture', validators=[FileRequired()])

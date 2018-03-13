""" Form with data required to upload a profile picture """
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired


class UploadProfilePictureForm(FlaskForm):
    """ Form with data required to upload a profile picture """
    profile_picture = FileField('Profile Picture', validators=[DataRequired()])

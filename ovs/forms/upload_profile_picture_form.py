""" Form with data required to upload a profile picture """
from imghdr import what

from flask_wtf import FlaskForm
from wtforms import FileField, ValidationError
from wtforms.validators import DataRequired


class UploadProfilePictureForm(FlaskForm):
    """ Form with data required to upload a profile picture """
    profile_picture = FileField('Profile Picture', validators=[DataRequired()])

    # def validate_profile_picture(form, field):
    #     """ Check's whether the image is actually a png """
    #     if field.data is None:
    #         raise ValidationError('File is empty')
    #     print(field.data)
    #     if what(None, h=field.data.decode()) != 'png':
    #         raise ValidationError('Image is not a png')

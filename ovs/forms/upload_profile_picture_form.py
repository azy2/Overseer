""" Form with data required to upload a profile picture """
import imghdr

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import ValidationError


class UploadProfilePictureForm(FlaskForm):
    """ Form with data required to upload a profile picture """
    profile_picture = FileField('Profile Picture', validators=[FileRequired()])

    def validate_profile_picture(form, field): # pylint: disable=no-self-argument, no-self-use
        """ Validates that the uploaded file is not empty and is a real PNG. """
        if field.data:
            contents = field.data.read()
            field.data.seek(0)
            if imghdr.what(None, h=contents) != 'png':
                raise ValidationError('Not a valid png')

        else:
            raise ValidationError('File is empty')

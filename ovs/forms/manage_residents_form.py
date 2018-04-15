""" Form with data required to edit a resident """
from flask_wtf import FlaskForm
from wtforms import  StringField, HiddenField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Length, Email

from ovs import db
from ovs.models.resident_model import Resident
from ovs.services.user_service import UserService
from ovs.services.room_service import RoomService





class ManageResidentsForm(FlaskForm):
    """ Form with data required to edit a resident """
    user_id = HiddenField('User id', validators=[DataRequired()])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    first_name = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=255), DataRequired()])
    room_number = StringField('Room Number', validators=[Length(max=255)])
    update_button = SubmitField('Update')
    delete_button = SubmitField('Delete')


    def validate_email(form, field): # pylint: disable=no-self-argument
        """ Checks whether email is unregistered. """
        user = UserService.get_user_by_id(form.user_id.data)
        if user:
            email = user.email
            if (field.data != email) and UserService.get_user_by_email(field.data) is not None:
                raise ValidationError('A user with that email already exists')
        else:
            raise ValidationError('No user with that ID')

    def validate_room_number(form, field): # pylint: disable=no-self-argument, no-self-use
        """ Checks whether room number exists """
        if field.data != '' and RoomService.get_room_by_number(field.data) is None:
            raise ValidationError("Room doesn't exist")

    def validate_user_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided user_id exists.
        This is to thwart malicious input.
        """
        if db.session.query(Resident).filter(Resident.user_id == field.data).count() == 0:
            raise ValidationError('Resident does not exist')

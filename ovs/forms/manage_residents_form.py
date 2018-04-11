""" Form with data required to edit a resident """
from flask_wtf import FlaskForm
from wtforms import  StringField, HiddenField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Length, Email

from ovs import db
from ovs.forms.validators import EmailRegistered
from ovs.models.resident_model import Resident
from ovs.services.user_service import UserService
from ovs.services.room_service import RoomService


def validate_user_id(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided user_id exists.
    This is to thwart malicious input.
    """
    if db.session.query(Resident).filter(Resident.user_id == field.data).count() == 0:
        raise ValidationError('Resident does not exist')


class ManageResidentsForm(FlaskForm):
    """ Form with data required to edit a resident """
    user_id = HiddenField('User id', validators=[DataRequired(), validate_user_id])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    first_name = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=255), DataRequired()])
    room_number = StringField('Room Number', validators=[Length(max=255)])
    update_button = SubmitField('Update')
    delete_button = SubmitField('Delete')


    def validate_email(form, field):
        email = UserService.get_user_by_id(form.user_id.data).first().email
        if (field.data != email) and UserService.get_user_by_email(field.data) is not None:
            raise ValidationError('A user with that email already exists')

    def validate_room_number(form, field):
        if field.data != '' and RoomService.get_room_by_number(field.data).one_or_none() is None:
            raise ValidationError("Room doesn't exist")

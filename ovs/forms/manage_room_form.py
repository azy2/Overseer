""" Form with data required to edit a room """
from flask_wtf import FlaskForm
from wtforms import  StringField, HiddenField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from ovs import db
from ovs.models.room_model import Room
from ovs.services.room_service import RoomService


class ManageRoomForm(FlaskForm):
    """ Form with data required to edit a resident """
    room_id = HiddenField('Room id', validators=[DataRequired()])
    room_number = StringField('Room Number', validators=[Length(min=1, max=255), DataRequired()])
    status = StringField('Status', validators=[Length(min=1, max=255), DataRequired()])
    room_type = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    update_button = SubmitField('Update')
    delete_button = SubmitField('Delete')

    def validate_room_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided user_id exists.
        This is to thwart malicious input.
        """
        if db.session.query(Room).filter(Room.room_id == field.data).count() == 0:
            raise ValidationError('Room does not exist')

    def validate_room_number(form, field): # pylint: disable=no-self-argument
        """ Checks whether email is unregistered. """
        room = RoomService.get_room_by_id(form.room_id.data)
        if room:
            number = room.room_number
            if (field.data != number) and RoomService.get_room_by_number(field.data) is not None:
                raise ValidationError('A room with that number already exists')
        else:
            raise ValidationError('No room with that ID')

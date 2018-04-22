""" Form with data required to edit a room """
from flask_wtf import FlaskForm
from wtforms import  StringField, HiddenField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from ovs.models.room_model import Room
from ovs.services.room_service import RoomService


class ManageRoomForm(FlaskForm):
    """ Form with data required to edit a room """
    room_id = HiddenField('Room id', validators=[DataRequired()])
    room_number = StringField('Room Number', validators=[Length(min=1, max=255), DataRequired()])
    status = StringField('Status', validators=[Length(min=1, max=255), DataRequired()])
    room_type = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    update_button = SubmitField('Update')
    delete_button = SubmitField('Delete')

    def validate_room_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided room_id exists.
        This is to thwart malicious input.

        Args:
            form: The ManageRoomForm that was submitted.
            field: The room_id field.

        Raises:
            ValidationError: If the room_id already exists.
        """
        if Room.query.filter_by(id=field.data).count() == 0:
            raise ValidationError('Room does not exist')

    def validate_room_number(form, field): # pylint: disable=no-self-argument
        """
        Checks whether room_number is unique.

        Args:
            form: The ManageRoomForm that was submitted.
            field: The room_number field.

        Raises:
            ValidationError: If the room_number already exists.
        """
        room = RoomService.get_room_by_id(form.room_id.data)
        if room:
            number = room.number
            if (field.data != number) and RoomService.get_room_by_number(field.data) is not None:
                raise ValidationError('A room with that number already exists')
        else:
            raise ValidationError('Room does not exist')

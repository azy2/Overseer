""" Form with data required to register a room """
from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError

from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService


class RegisterRoomForm(FlaskForm):
    """ Form with data required to register a room """
    room_number = StringField('Room Number',
                              validators=[validators.Length(min=1, max=255), validators.DataRequired()])
    room_status = StringField('Room Status',
                              validators=[validators.Length(min=1, max=255), validators.DataRequired()])
    room_type = StringField('Room Type',
                            validators=[validators.Length(min=1, max=255), validators.DataRequired()])
    occupants = StringField('Room Occupants (by email and delimited by semicolons):',
                            validators=[validators.Optional()])

    def validate_room_number(form, field):
        if RoomService.get_room_by_number(field.data).one_or_none() is not None:
            raise ValidationError('A room with that number already exists')

""" Form with data required to register a room """
from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError

from ovs.services.room_service import RoomService
from ovs.services.resident_service import ResidentService


class RegisterRoomForm(FlaskForm):
    """ Form with data required to register a room """
    room_number = StringField('Room Number',
                              validators=[validators.Length(min=1, max=255), validators.DataRequired()])
    room_status = StringField('Room Status',
                              validators=[validators.Length(min=1, max=255), validators.DataRequired()])
    room_type = StringField('Room Type',
                            validators=[validators.Length(min=1, max=255), validators.DataRequired()])
    occupants = StringField('Room Occupants (Comma separated list of emails):',
                            validators=[validators.Optional()])

    def validate_room_number(form, field): # pylint: disable=no-self-argument, no-self-use
        """ Validates that room number does not already exist """
        if RoomService.get_room_by_number(field.data) is not None:
            raise ValidationError('A room with that number already exists')

    def validate_occupants(form, field): # pylint: disable=no-self-argument, no-self-use
        """ Validates thet occupants exist and don't already have a room """
        occupants = ''.join(field.data.split()).split(',')
        for occupant in occupants:
            resident = ResidentService.get_resident_by_email(occupant)
            if resident is None:
                raise ValidationError('One of the emails is not a resident')

            if str(resident.room_number) != '':
                raise ValidationError('One of the residents already has a room')

""" Form with data required to register a room """
from flask_wtf import FlaskForm
from wtforms import StringField, validators


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

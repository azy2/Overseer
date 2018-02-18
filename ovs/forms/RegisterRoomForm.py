from flask_wtf import FlaskForm
from wtforms import StringField, validators

class RegisterRoomForm(FlaskForm):
    room_number = StringField('Room Number', [validators.Length(min=1, max=255), validators.DataRequired()])
    room_status = StringField('Room Status', [validators.Length(min=1, max=255), validators.DataRequired()])
    room_type = StringField('Room Type', [validators.Length(min=1, max=255), validators.DataRequired()])
    occupants = StringField('Room Occupants (by email and delimited by semicolons):', [validators.Optional()])

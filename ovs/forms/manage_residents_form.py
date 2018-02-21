""" Form with data required to edit a resident """
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length
from ovs.models.resident_model import Resident
from ovs import app
db = app.database.instance()


class ManageResidentsForm(FlaskForm):
    """ Form with data required to edit a resident """
    user_id = StringField('User id', validators=[DataRequired()])
    room_number = StringField('Room Number', validators=[Length(min=1, max=255), DataRequired()])

    def validate_user_id(form, field):
        if db.query(Resident).filter(Resident.user_id == field.data).count() == 0:
            raise ValidationError('Resident does not exist')

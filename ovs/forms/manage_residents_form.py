""" Form with data required to edit a resident """
from flask_wtf import FlaskForm
from wtforms import  StringField, ValidationError
from wtforms.validators import DataRequired, Length, Email

from ovs import db
from ovs.models.resident_model import Resident


def validate_user_id(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided user_id exists.
    This is to thwart malicious input.
    """
    if db.session.query(Resident).filter(Resident.user_id == field.data).count() == 0:
        raise ValidationError('Resident does not exist')


class ManageResidentsForm(FlaskForm):
    """ Form with data required to edit a resident """
    user_id = StringField('User id', validators=[DataRequired(), validate_user_id])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    first_name = StringField('First Name', validators=[Length(min=1, max=255), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=255), DataRequired()])
    room_number = StringField('Room Number', validators=[Length(min=1, max=255), DataRequired()])
